"""
- Title:            Standalone Semantic Similarity Search Module with Cache. Wrapper on top of Sentence Transformer and
                    Pandas)
- Project/Topic:    Utils Tabular Data. Practical functions for Data Science
- Author/s:         Angel Martinez-Tenor
- Dev Date:         2017 - 2022

- Status:           Planning
"""

from __future__ import annotations

import shutil
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from time import time
from typing import ClassVar

import numpy as np
import pandas as pd
import requests
import torch
import urllib3
from sentence_transformers import SentenceTransformer, util

from smart_data_science import logger
from smart_data_science.analysis.info import ratio_to_text
from smart_data_science.process.transform import fill_nan_on_index

log = logger.get_logger(__name__)

# Default Cosine similarity threshold for search() method (used if no external threshold is provided)
MATCH_THRESHOLD = 0.85

EMBEDDINGS_CACHE_PATH = Path("data_cache/embeddings.parquet")
ST_MODEL_PATH = "sentence-transformers/all-MiniLM-L6-v2"
SIZE_EMBEDDING_VECTOR = 384
LOCAL_MODEL_PATH = Path("models")

# local_path_model = LOCAL_MODEL_PATH / ST_MODEL_PATH.replace("/", "_")


def clean_text_series_embedding(text_series: pd.Series) -> pd.Series:
    """Apply Custom text cleaning for Embeddings. This function could be moved to the ETL module
    Args:
        text_series (pd.Series): Text Series
    Returns:
        pd.Series: Normalized Text Series cleaned for embedding
    """
    ds = text_series.copy()
    ds = ds.astype(str)
    ds = ds.replace(r"[/,|,_,-]", " ", regex=True)
    ds = ds.replace(r"\s+", " ", regex=True)
    ds = ds.str[:200]  # New: Reduce size to avoid memory error

    return ds


def get_text_to_embed(df: pd.DataFrame, cols_to_embed: list[str]) -> pd.Series:
    """Generate and Return the Text Series used for similarity search from the given table
    Only the variables in selected variables in SEMANTIC_SEARCH_COLUMNS are joined for the semantic search
    Args:
        df (pd.DataFrame): input table (contains the semantic search columns)
    Returns:
        pd.Series: Text Series to encode for similarity search
    """
    search_text_series = df[cols_to_embed].agg(". ".join, axis=1)
    search_text_series = clean_text_series_embedding(search_text_series)  # TO TEST: normalize before joining
    return search_text_series


def get_most_common_words(text_series: pd.Series, k: int = 10, sep: str = " ") -> pd.Series:
    """Return the 'k' top most frequent words from the input text series as a string separated by 'sep'
    Used to get top parts from work elements previously filtered with clean_text_series_embedding (EXP)
    Args:
        text_series (pd.Series): Text Series
        k (int, optional): Number of top most frequent words. Defaults to 10.
        sep (str, optional): Separator. Defaults to " ".
    Returns:
        pd.Series: Text Series with 'k' top most frequent words only
    """
    ds = text_series.copy()
    ds = ds.apply(lambda x: Counter(x.split(" ")).most_common(k))
    ds = ds.apply(lambda x: [item[0] for item in x])
    ds = ds.apply(lambda x: sep.join(map(str, x)))
    return ds


def load_sentence_transformer_model(
    remote_model_path: str | Path = ST_MODEL_PATH,
    local_path: str | Path = LOCAL_MODEL_PATH,  # local_path_model=local_path_model)
) -> SentenceTransformer:
    """Import/Update the desired sentence transformer model to a local path.
    In case of connection error, import the local model directly without checking the remote model

    Args:
        remote_model_path (Path, optional): Sentence Transformer model/path. Defaults to ST_MODEL_PATH.
        local_path (Path, optional): Local path to store the Sentence Transformer model. Defaults to LOCAL_MODEL_PATH

    Returns:
        SentenceTransformer: Sentence Transformer (BERT) Model
    """
    remote_model_path = Path(str(remote_model_path).replace("/", "_"))
    try:
        model = SentenceTransformer(remote_model_path, cache_folder=local_path)
    except (
        urllib3.exceptions.NewConnectionError,
        requests.exceptions.ConnectionError,
        requests.exceptions.HTTPError,
    ):  # as network_error:
        local_path_model = local_path / remote_model_path
        log.warning("   Network error")  # {network_error}") Output simplification requested
        log.info(f"   Loading Local Model: {local_path_model}")
        try:
            model = SentenceTransformer(local_path_model, cache_folder=LOCAL_MODEL_PATH)
        except TypeError:  # as path_error:
            error_string = (
                "\nNeither Internet Connection Nor Model Path Found. "
                f"Please, copy your BERT model folder to {local_path_model}\n"
            )
            # raise TypeError(error_string) from path_error. To Improve: Export to log
            log.critical(error_string)  # Output simplification requested
            sys.exit(1)

    return model


def generate_embedding(  # pylint: disable=too-many-arguments, too-many-statements
    ds: pd.Series,
    model: SentenceTransformer = None,
    batch_id: str = "default",
    cache: bool = True,
    cache_path: Path = None,
) -> torch.Tensor:
    """Return a Torch Tensor of the BERT embeddings of the input Series.
        If cache=True and a cache_path is provided, it will save the new vectorized texts in a partition od the parquet
        file identified by batch_id (not needed when loading the whole embedding cache)

    Args:
        ds (pd.Series): Pandas Series with the column to search (the index won't be used)
        model (SentenceTransformer): Pre-trained Sentence Transformer model
        batch_id (str, optional): Id of the batch (e.g.: a batch_id=A. It will be used for generating a partitioned
            parquet file. Defaults to "default".
        cache (bool, optional): Enable embedding cache. It will load/save all the vectorized texts. Defaults to True.
        cache_path (Path, optional): Path of the embedding cache e.g.: data_cache/embedding.parquet: . Defaults to None.

    Returns:
        torch.Tensor: Matrix with the BERT-extracted vectors of the input texts (ds).
        1 row per input text (size of ds), 1 column per BERT element (size = 384 with model all-MiniLM-L6-v2)
    """

    if cache:
        try:
            assert cache_path is not None
        except AssertionError:
            log.critical(
                "Embedding cache=True but cache_path=None. Please call \
                generate_embedding with cache_path (e.g.: Path(embedding.parquet)"
            )
            sys.exit(1)

    # assert batch_id != "nan", log.critical("'nan' is not a valid name for a batch_id")
    try:
        assert batch_id != "nan"
    except AssertionError:
        log.critical("'nan' is not a valid name for a batch_id")
        sys.exit(1)

    # Create Embedding Table to fill (all NaNs). The code can be simplified by using an empty table  with indexes only
    # The current implementation (more complex) easies the debug
    vector_cols = [f"v{i}" for i in range(SIZE_EMBEDDING_VECTOR)]
    usecols = vector_cols + ["batch_id"]
    df = pd.DataFrame(index=ds.values, columns=usecols)
    original_index = df.index.copy()
    df.index = df.index.astype(str)
    n_samples = df.shape[0]

    # Create Empty Embedding Table Cache
    df_cache = pd.DataFrame()

    # Check & Load cache
    if cache and cache_path.exists():
        try:
            df_cache = pd.read_parquet(cache_path)
            df_cache = df_cache[~df_cache.index.duplicated(keep="first")]
            df_cache.index = df_cache.index.astype(str)  # fix parquet issue
        except MemoryError:
            log.error(
                " Memory error while reading the cache. Disabling cache: The embedding process will take \
                much longer"
            )
            cache = False

    # Fill embedding table with cache
    # df = df.fillna(df_cache)  # Doesn't work with duplicated index (index error). Workaround: Adhoc function
    df = fill_nan_on_index(df, df_cache)

    n_samples_found_in_cache = df["batch_id"].notna().sum()  # pylint: disable=unsubscriptable-object
    log.info(f"{'  Samples found in cache:':<38} {ratio_to_text(n_samples_found_in_cache, n_samples)}")

    # If all the embeddings were found in cache, just return the matrix with the vectorized texts
    if n_samples_found_in_cache == n_samples:
        return torch.from_numpy(df[vector_cols].values.astype(np.float32))  # pylint: disable=unsubscriptable-object

    # Get the Embeddings of the rest of the samples (text vectorization)
    df_to_encode = df[df["batch_id"].isna()].copy()  # pylint: disable=unsubscriptable-object

    # No need to encode duplicated texts (the original structure will be reconstructed using df)
    df_to_encode = df_to_encode[~df_to_encode.index.duplicated(keep="first")]

    # # Load the embedding model if not available
    # if model is None and Semantic.model is None:
    #     log.info("   Loading embedding model to vectorize texts...")
    #     model = load_sentence_transformer_model()
    # elif Semantic.model is not None:
    #     model = Semantic.model

    # Compute embedding. optimal batch encoding.  Do not use apply (nor swifter), it will take at twice as long
    v_embeddings = model.encode(df_to_encode.index, convert_to_numpy=True, show_progress_bar=True)

    Semantic.default_model = model  # speed up future BER model loads
    # TO IMPROVE: High processing time issue can be found with >100k samples (no detected so far)

    # Generate a table from of encoded/vectorized  (includes batch_id)
    df_embeddings = pd.DataFrame(v_embeddings, index=df_to_encode.index)
    df_embeddings = df_embeddings.add_prefix("v")  # no numbers as columns in parquet
    df_embeddings["batch_id"] = batch_id
    df_embeddings[vector_cols] = df_embeddings[vector_cols].astype(np.float32)

    # join found in cache (if any) with new computed vectors(embeddings)
    df = fill_nan_on_index(df, df_embeddings)
    df[vector_cols] = df[vector_cols].astype(np.float32)

    # assert df["batch_id"].isna().sum() == 0, log.critical("Incomplete Vectorization")
    try:
        assert df["batch_id"].isna().sum() == 0
    except AssertionError:
        log.critical("Incomplete Vectorization")
        sys.exit(1)

    # assert "nan" not in df["batch_id"].values, log.critical("'nan' is not a valid name for a batch_id")
    try:
        assert "nan" not in df["batch_id"].values
    except AssertionError:
        log.critical("'nan' is not a valid name for a batch_id")
        sys.exit(1)

    if cache:
        update_cache(df, df_cache, cache_path)
        # log.info(f"({round(time()-t_start)}s)")
        # log.info(f"Embedding cache location: {self.cache_path}")

    # assert original_index.equals(df.index), log.critical("Embeddings indexes changed")
    try:
        assert original_index.equals(df.index)
    except AssertionError:
        log.critical("Embeddings indexes changed")
        sys.exit(1)

    return torch.from_numpy(df[vector_cols].values.astype(np.float32))


def update_cache(df: pd.DataFrame, df_cache: pd.DataFrame, cache_path: Path | str) -> None:
    """
    Update the embedding cache with the new embeddings
    Args:
        df (pd.DataFrame): Embeddings table with the new embeddings
        df_cache (pd.DataFrame): Embeddings table with the cached embeddings
        cache_path (Path|str): Path of the embedding cache e.g.: data_cache/embedding.parquet
    """
    cache_path = Path(cache_path)
    log.info(" - Updating Cache ...")
    # t_start = time()
    df_cache = df.copy() if df_cache.empty else pd.concat([df_cache, df])
    # Avoid duplicated texts in cache (even in different partitions of the cache)
    df_cache = df_cache[~df_cache.index.duplicated(keep="first")]
    df_cache["batch_id"] = df_cache["batch_id"].astype(str)
    # df_cache[vector_cols] = df_cache[vector_cols].astype(np.float32)
    # df_cache.index = df_cache.index.astype(str)
    if cache_path.exists():
        # Save a backup of embeddings before freeing the embedding path
        backup_filename = f"{cache_path.stem}_BACKUP{cache_path.suffix}"
        backup_cache_path = cache_path.parent / backup_filename
        if backup_cache_path.exists():
            shutil.rmtree(backup_cache_path)
        shutil.copytree(cache_path, backup_cache_path)
        shutil.rmtree(cache_path)
    df_cache.to_parquet(cache_path, partition_cols=["batch_id"])  # compression='gzip')


@dataclass
class Semantic:  # pylint: disable=too-many-instance-attributes
    """Semantic Similarity Search Class: Apply a pre-trained Bert model to encode a reference and a target table.
    Constructor: load the input data: preprocessed reference & target tables
    Main Args:
        df_ref (pd.DataFrame): Preprocessed Reference table
        df_target (pd.DataFrame): Preprocessed target table
        id_col (str): Main id column. The input dataframes, embeddings & similarity matrix will be sorted by this id
        id_col_description (str): Caption/description of id_col to be used as output text
        cols_to_embed (list[str]): Columns that will be concatenated and embedded
        ref_id (str): Unique Id for the Reference table (e.g.: table id)
        target_id (str): Unique Id for the Target table (e.g.: table id)
        cache_embedding (bool, optional): Use cache: search in previously saved embedding vectors (if exists).
           Also saves the pair text & vectorize text as a distributed dataframe in Parquet. Defaults to True
        cache_path (Path, optional): Path of embeddings cache. Defaults to EMBEDDINGS_CACHE_PATH
        default_model (ClassVar[SentenceTransformer], optional): Pre-trained Bert model. Defaults to None

    NOTE: THE RESULTED EMBEDDINGS & SIMILARITY MATRIX ARE ALWAYS SORTED BY THE VALUES OF 'ID_COL' (ascending order)"""

    df_ref: pd.DataFrame
    df_target: pd.DataFrame
    id_col: str
    id_col_description: str
    cols_to_embed: list[str]
    ref_id: str
    target_id: str
    cache_embedding: bool = True
    cache_path: Path = EMBEDDINGS_CACHE_PATH
    default_model: ClassVar[SentenceTransformer] = None

    def __post_init__(self) -> None:
        """Post-init processing. Initialize field values"""

        self.cols_to_get_from_ref: list[str] = None
        self.cols_from_ref_to_target: list[str] = None
        self.r_embedding: torch.Tensor = None
        self.t_embedding: torch.Tensor = None
        self.similarity_matrix: torch.Tensor = None
        self.df_result = pd.Series(dtype="object")
        self.metric_matched: float = None
        self.metric_accuracy_existing: float = None
        self.match_threshold = MATCH_THRESHOLD  # set in search method
        self.model = None

        # assert self.id_col in self.df_ref.columns, log.critical(f"{self.id_col} not found in the reference table")
        try:
            assert self.id_col in self.df_ref.columns
        except AssertionError:
            log.critical(f"{self.id_col} not found in the reference table")
            sys.exit(1)

        # assert self.id_col in self.df_target.columns, log.critical(f"{self.id_col} not found in the target table")
        try:
            assert self.id_col in self.df_target.columns
        except AssertionError:
            log.critical(f"{self.id_col} not found in the target table")
            sys.exit(1)

        self.df_ref = self.df_ref.astype(str).sort_values(self.id_col).reset_index(drop=True)
        self.df_target = self.df_target.astype(str).sort_values(self.id_col).reset_index(drop=True)

        df_ref_size_str = f"{self.df_ref.shape[0]}, {self.df_ref.shape[1]}"
        df_target_size_str = f"{self.df_target.shape[0]}, {self.df_target.shape[1]}"
        log.info("Input Data")
        log.info(f"{' - Reference table Size:':<38} {df_ref_size_str:>10}")
        log.info(f"{' - Target table Size:':<38} {df_target_size_str:>10}")

        log.info("Getting Embeddings")

        # Load the embedding model if not available
        if Semantic.default_model is None:
            log.info(" - Loading embedding model to vectorize texts")
            Semantic.default_model = load_sentence_transformer_model()

        self.model = Semantic.default_model

        log.info(f"{' - Columns Embedded:':<38} {', '.join(self.cols_to_embed)}")
        log.info(" - Target Embeddings")
        self.df_target["search_text"] = get_text_to_embed(self.df_target, self.cols_to_embed)

        self.t_embedding = generate_embedding(
            self.df_target["search_text"],
            self.model,
            batch_id=self.target_id,
            cache=self.cache_embedding,
            cache_path=self.cache_path,
        )

        log.info(" - Reference Embeddings")
        self.df_ref["search_text"] = get_text_to_embed(self.df_ref, self.cols_to_embed)
        self.r_embedding = generate_embedding(
            self.df_ref["search_text"],
            self.model,
            batch_id=self.ref_id,
            cache=self.cache_embedding,
            cache_path=self.cache_path,
        )

    def get_similarity(self) -> torch.Tensor:
        """Get the Cosine similarity between target & reference tables
        Returns:
            torch.Tensor: Cosine similarity matrix of embeddings. Horizontal axis: target. Vertical axis: Reference
        """
        similarity_matrix = util.pytorch_cos_sim(self.t_embedding, self.r_embedding)
        self.similarity_matrix = similarity_matrix
        return similarity_matrix

    # @profile
    def search(  # pylint: disable = too-many-statements
        self, cols_to_get_from_ref: list[str], match_threshold: float = MATCH_THRESHOLD
    ) -> pd.DataFrame:
        """Perform a semantic search on cols_to_embed and return an extended target table with get_reference_cols from
        the reference table. The new columns will be preceded by the prefix h_ (historical)

        Args:
            cols_to_get_from_ref (list[str]): Columns of the matched reference table copied to the extended target table
            SEMANTIC_MATCH_THRESHOLD (float, optional): A cosine similarity >= threshold will be labeled as a match
                Defaults to SEMANTIC_MATCH_THRESHOLD.
        Returns:
             pd.DataFrame: Extended Target table after semantic search with new columns from ref table (prefix h_)

        This method also updates the following attributes:
            self.df_result (pd.DataFrame): Same as returned table
            self.similarity_matrix (torch.Tensor) = similarity_matrix
        """

        # assert self.df_ref.shape[0], log.critical("Reference table is empty")
        try:
            assert self.df_ref.shape[0]
        except AssertionError:
            log.critical("Reference table is empty")
            sys.exit(1)

        # assert self.df_target.shape[0], log.critical(
        #     "Target table is empty"
        # )  # also avoids division by 0 with df_result.shape[0]
        try:
            assert self.df_target.shape[0]
        except AssertionError:
            log.critical("Target table is empty")
            sys.exit(1)

        df_ref = self.df_ref
        df_target = self.df_target
        id_col = self.id_col
        self.match_threshold = match_threshold
        self.cols_to_get_from_ref = cols_to_get_from_ref
        # self.r_embedding & self.t_embedding are directly used from self.get_similarity()

        # Perform Similarity Search
        log.info("Matching tables ....")
        t_start = time()
        similarity_matrix = self.get_similarity()
        # similarity_matrix = util.pytorch_cos_sim(t_embedding, r_embedding)  (obsolete)

        # Extract top match:
        max_tensor = similarity_matrix.max(dim=1)  # axis=1)  # TO CHECK
        # similarity_matrix[[73]].topk(5)  # get top 5 results instead of max only
        h_table_indexes = pd.Series(max_tensor.indices, name="h_index")  # h_index : index of the reference table
        h_table_score = pd.Series(max_tensor.values, name="sim").round(3)
        df_search = pd.concat([h_table_indexes, h_table_score], axis=1)
        df_search.index.name = "t_index"

        # Generate Result Table
        df_result = df_target.copy().join(df_search)
        # New fields with values from the reference table matched with format h_<variable>):
        self.cols_from_ref_to_target = []  # only used to sort variables of the final predicted table
        for col in cols_to_get_from_ref:
            historical_col_name = f"h_{col}"
            df_result[historical_col_name] = df_result["h_index"].apply(
                lambda x: df_ref.iloc[x][col]  # pylint: disable=cell-var-from-loop, disable=undefined-loop-variable
            )
            self.cols_from_ref_to_target.append(historical_col_name)
        log.info(f"   tables Matched in {round(time()-t_start)}s")

        # Postprocess results
        df_result["sim"] = df_result["sim"].astype(float).round(3)
        df_result["match"] = np.where(df_result["sim"] > match_threshold, True, False)

        # assert df_result.shape[0] == df_result[self.id_col].nunique(), log.critical(
        #     "The Predicted table contains duplicated ids"
        # )
        try:
            assert df_result.shape[0] == df_result[self.id_col].nunique()
        except AssertionError:
            log.critical("The Predicted table contains duplicated ids")
            sys.exit(1)

        # Print Results:
        log.info("Semantic Search Results")
        log.info(f"{' - Avg Similarity Score:':<38} {df_result['sim'].mean():>10.3f}")

        n_match = df_result[df_result["match"]].shape[0]
        aux_text = f" - Matches (sim>{match_threshold:.2f}):"
        self.save_metric_matched(n_match, df_result, aux_text)
        # The following metrics are only available if the id_col of the ref is extracted
        id_col_from_ref = f"h_{id_col}"
        if id_col_from_ref in df_result:
            df_existing_id = df_result[df_result[id_col].isin(df_ref[id_col].unique())]
            df_matched_id = df_result[df_result[id_col] == df_result[id_col_from_ref]]
            self.metric_accuracy_existing = (
                df_matched_id.shape[0] / df_existing_id.shape[0] if df_existing_id.shape[0] else 0
            )
            existing_ration_str = (
                f"{df_matched_id.shape[0]}/{df_existing_id.shape[0]}" if df_existing_id.shape[0] else "N/A"
            )
            aux_text = f" - Existing {self.id_col_description} matched:"
            log.info(f"{aux_text:<38} {existing_ration_str:>10}" f" ({self.metric_accuracy_existing:.1%})")

            # Metrics for new ids:
            df_new_ids = df_result[~df_result[id_col].isin(df_ref[id_col].unique())]
            n_match_new = df_new_ids[df_new_ids["match"]].shape[0]
            reliability_new = (n_match_new) / df_new_ids.shape[0] if df_new_ids.shape[0] else 0
            new_match_str = f"{n_match_new}/{df_new_ids.shape[0]}" if df_new_ids.shape[0] else "N/A"

            aux_text = f" - New {self.id_col_description}. Avg Sim Score:"
            log.info(f"{aux_text:<38} {df_new_ids['sim'].mean():>10.3f}")
            aux_text = f" - New {self.id_col_description}. Matches:"  # (sim>{match_threshold:.2f}):"
            log.info(
                f"{aux_text:<38} {new_match_str:>10} ({reliability_new:.1%})"
                # f" - New {self.id_col_description}. Matches (sim>{match_threshold:.2f}) "
                # f"{new_match_str:>14} ({reliability_new:.1%})"
            )

            # Assign labels - Search Result
            df_result["new_id"] = False
            df_result.loc[df_new_ids.index, "search_result"] = True
            df_result["search_result"] = "Existing id"
            df_result.loc[df_new_ids.index, "search_result"] = "New id"
            dict_match = {True: "matched", False: "not matched"}
            df_result["search_result"] = df_result["search_result"] + " " + df_result["match"].map(dict_match)

            # Postprocess Stage: After semantic Search, the prediction of all WE with search result
            #  'Existing id not matched'  will be matched with the WE with same ID of the reference table
            df_existing_ids_low_sim = df_result.loc[df_result["search_result"] == "Existing id not matched"].copy()
            if df_existing_ids_low_sim.empty is False:
                # log.info("Post-process Stage")
                # log.info(" - Force non-match semantic matches of Existing ids to matches by id (direct assignation)")
                df_ref_temp = df_ref.set_index(id_col, drop=False)
                for col in cols_to_get_from_ref:
                    historical_col_name = f"h_{col}"
                    df_existing_ids_low_sim[historical_col_name] = df_existing_ids_low_sim[id_col].apply(
                        lambda x: df_ref_temp.loc[x][col]  # pylint: disable=cell-var-from-loop
                    )
                df_existing_ids_low_sim["search_result"] = "Existing id matched by id"
                df_existing_ids_low_sim["match"] = True
                df_result.update(df_existing_ids_low_sim)
                aux_text = f" - Adding {self.id_col_description} Matched by id only"
                log.info(f"{aux_text:<38} {df_existing_ids_low_sim.shape[0]:>14}")

                # Update match (found)
                # Code similar to the above one, but extracting this into function won't add simplicity here
                n_match = df_result[df_result["match"]].shape[0]
                self.save_metric_matched(n_match, df_result, " - Global Found/Matches (match=True)")

                df_result["match"] = df_result["match"].astype(bool)  # avoid object type with NaNs

            log.info(f"\n{df_result['search_result'].value_counts().to_frame()}\n")
            # log.info(f"Type of Search \t {self.id_col_description}")
            # for i in df_result["search_result"].value_counts().to_string().split("\n"):
            #    log.info(f"   {i}")

        pred_table_size = f"{df_result.shape[0]}, {df_result.shape[1]}"
        log.info(f" - Predicted table Size: {pred_table_size}\n")

        # Sort columns
        all_cols = list(df_result)
        search_result_cols = ["search_text", "sim", "match", "new_id", "search_result"]
        sorted_cols = [self.id_col] + self.cols_to_embed + search_result_cols
        sorted_cols = sorted_cols + self.cols_from_ref_to_target + all_cols
        df_result = df_result[sorted_cols].copy()
        df_result = df_result.loc[:, ~df_result.columns.duplicated()]

        # save for analysis
        self.df_result = df_result
        # self.similarity_matrix = similarity_matrix # already saved in get_similarity()

        return df_result

    def save_metric_matched(self, n_match: int, df_result: pd.DataFrame, aux_text: str):
        """Save metrics of matched elements

        Args:
            n_match (int): Number of matches
            df_result (pd.DataFrame): Dataframe with results
            aux_text (str): Text to print
        """
        self.metric_matched = (n_match) / df_result.shape[0]  # df_result.shape[0] cannot be 0 (passed above)
        match_ratio_str = f"{n_match}/{df_result.shape[0]}"
        log.info(f"{aux_text:<38} {match_ratio_str:>10} ({self.metric_matched:.1%})")
