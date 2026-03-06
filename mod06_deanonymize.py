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
    anon_columns = set(anon_df.columns)
    aux_columns = set(aux_df.columns)

    anon_columns.discard('anon_id')
    aux_columns.discard('name')

    matching_columns = anon_columns.intersection(aux_columns)

    merge = pd.merge(anon_df, aux_df, on=matching_columns, how='inner')
    count = merge.groupby('anon_id').size()
    unique_matches = count[count == 1].index

    matches_df = merge[merge['anon_id'].isin(unique_matches)][['anon_id', 'name']]
    matches_df.rename(columns={'name': 'matched_name'}, inplace=True)

    return matches_df


def deanonymization_rate(matches_df, anon_df):
    """
    Compute the fraction of anonymized records
    that were uniquely re-identified.
    """
    total_anon_records = len(anon_df)
    return len(matches_df) / total_anon_records if total_anon_records > 0 else 0

