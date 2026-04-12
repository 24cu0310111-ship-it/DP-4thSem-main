import { useState, useEffect, useCallback } from 'react';
import type { Complaint, ComplaintStatus, PriorityLevel } from '../types';
import { complaintService } from '../services/complaintService';

export function useComplaints(mode: 'user' | 'admin' = 'user') {
  const [complaints, setComplaints] = useState<Complaint[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchComplaints = useCallback(async (filters?: {
    status?: ComplaintStatus;
    priority?: PriorityLevel;
    category?: string;
  }) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = mode === 'admin'
        ? await complaintService.getAdminComplaints(filters)
        : await complaintService.getUserComplaints(filters);
      setComplaints(response.data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch complaints');
    } finally {
      setIsLoading(false);
    }
  }, [mode]);

  useEffect(() => {
    fetchComplaints();
  }, [fetchComplaints]);

  return { complaints, isLoading, error, refetch: fetchComplaints };
}
