import { useState, useEffect, useCallback } from 'react';
import type { ServiceProvider, ComplaintCategory } from '../types';
import { providerService } from '../services/providerService';

export function useProviders(category?: ComplaintCategory, area?: string) {
  const [providers, setProviders] = useState<ServiceProvider[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchProviders = useCallback(async (filters?: {
    category?: ComplaintCategory;
    area?: string;
    platform?: string;
    min_rating?: number;
  }) => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await providerService.getProviders(filters || { category, area });
      setProviders(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch providers');
    } finally {
      setIsLoading(false);
    }
  }, [category, area]);

  useEffect(() => {
    fetchProviders();
  }, [fetchProviders]);

  return { providers, isLoading, error, refetch: fetchProviders };
}
