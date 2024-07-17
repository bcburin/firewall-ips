import { useCallback, useEffect, useState } from 'react';

export interface PaginatedResponse<T> {
    data: T[];
    total: number;
}

interface PaginationModel {
  page: number;
  pageSize: number;
}

export const usePaginatedData = <T,>(fetchData: (page: number, pageSize: number) => Promise<PaginatedResponse<T>>) => {
  const [data, setData] = useState<T[]>([]);
  const [total, setTotal] = useState(0);
  const [paginationModel, setPaginationModel] = useState<PaginationModel>({ page: 0, pageSize: 25 });
  const [loading, setLoading] = useState<boolean>(false);

  const getData = useCallback(async () => {
    setLoading(true);
    try {
      const response = await fetchData(paginationModel.page, paginationModel.pageSize);
      setData(response.data);
      setTotal(response.total);
    } catch (e) {
      console.log(e);
    } finally {
      setLoading(false);
    }
  }, [fetchData, paginationModel]);

  useEffect(() => {
    getData();
  }, [getData]);

  return { data, total, paginationModel, setPaginationModel, getData, loading };
};
