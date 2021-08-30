### pageJsonNoTitles:
1. Takes:
   * Excel file with two columns 'record_id' and 'files'
2. Output:
   * Page json for ingest into dlgamdin
   * No page titles, only sequential numbers starting at 1 (1, 2, 3...)


### pageJsonWithTitles:
1. Takes:
   * Excel file with two columns per worksheet: 'image' and 'page'
   * Each worksheet should be named with the record_id
2. Output:
   * Page json for ingest into dlgamdin
   * Includes page numbers for ordering and title for display in Mirador