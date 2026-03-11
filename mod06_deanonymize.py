import pandas as pd

def load_data(anonymized_path, auxiliary_path):
    """
    Load anonymized and auxiliary datasets.
    """
    anon = pd.read_csv(anonymized_path)
    aux = pd.read_csv(auxiliary_path)
    return anon, aux


def link_records(anon_df, aux_df):
    """
    Attempt to link anonymized records to auxiliary records
    using exact matching on quasi-identifiers.

    Returns a DataFrame with columns:
      anon_id, matched_name
    containing ONLY uniquely matched records.
    """
    qi_cols = [c for c in anon_df.columns if c != "anon_id" and c in aux_df.columns] # Identify quasi-identifier columns by finding common columns (excluding anon_id)
    if not qi_cols:
        return pd.DataFrame(columns=["anon_id", "matched_name"])

    anon_counts = (
        anon_df.groupby(qi_cols, as_index=False) # Count occurrences of each QI combination in the anonymized dataset
        .size()
        .rename(columns={"size": "anon_count"})
    )
    aux_counts = (
        aux_df.groupby(qi_cols, as_index=False) # Count occurrences of each QI combination in the auxiliary dataset
        .size()
        .rename(columns={"size": "aux_count"})
    )

    unique_qi = anon_counts.merge(aux_counts, on=qi_cols, how="inner") # Only consider QI combinations present in both datasets
    unique_qi = unique_qi[
        (unique_qi["anon_count"] == 1) & (unique_qi["aux_count"] == 1)
    ][qi_cols] # Keep only QI combinations that are unique in both datasets

    if unique_qi.empty: # No unique matches found
        return pd.DataFrame(columns=["anon_id", "matched_name"])

    matches = (
        anon_df.merge(unique_qi, on=qi_cols, how="inner") # Keep only records with unique QI combinations
        .merge(aux_df[qi_cols + ["name"]], on=qi_cols, how="inner") # Join with auxiliary to get names
        .loc[:, ["anon_id", "name"]] # Keep only anon_id and name
        .rename(columns={"name": "matched_name"}) # Rename for clarity
        .drop_duplicates() # Ensure we only have unique matches
    )
    return matches


def deanonymization_rate(matches_df, anon_df):
    """
    Compute the fraction of anonymized records
    that were uniquely re-identified.
    """
    total = len(anon_df) # Total number of anonymized records
    if total == 0:
        return 0.0
    matched = matches_df["anon_id"].nunique() if "anon_id" in matches_df.columns else 0 # Count unique matched anon_ids
    return matched / total
