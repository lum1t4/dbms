'use client';

import { useEffect, useState } from 'react';
import { tissuesAPI } from '@/lib/api/tissues';
import type { Tissue } from '@/types';

export default function TissuesPage() {
  const [tissues, setTissues] = useState<Tissue[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchTissues() {
      try {
        setLoading(true);
        const data = await tissuesAPI.getAll();
        setTissues(data.tissues);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch tissues:', err);
        setError('Failed to load tissues. Please check if the backend is running.');
      } finally {
        setLoading(false);
      }
    }
    fetchTissues();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-lg">Loading tissues...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-destructive/10 border border-destructive text-destructive px-4 py-3 rounded">
        {error}
      </div>
    );
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold">Tissues</h1>
          <p className="text-muted-foreground mt-1">Manage tissue and organ information (Operation 1)</p>
        </div>
        {/* <Link href="/tissues/new">
          <Button>
            <Plus className="h-4 w-4 mr-2" />
            Add Tissue
          </Button>
        </Link> */}
      </div>

      <div className="bg-card rounded-lg border">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="border-b bg-muted/50">
              <tr>
                <th className="px-4 py-3 text-left text-sm font-medium">ID</th>
                <th className="px-4 py-3 text-left text-sm font-medium">Name</th>
                <th className="px-4 py-3 text-left text-sm font-medium">Description</th>
                <th className="px-4 py-3 text-left text-sm font-medium">Density</th>
                <th className="px-4 py-3 text-left text-sm font-medium">Vital</th>
                {/* <th className="px-4 py-3 text-right text-sm font-medium">Actions</th> */}
              </tr>
            </thead>
            <tbody>
              {tissues.length === 0 ? (
                <tr>
                  <td colSpan={6} className="px-4 py-8 text-center text-muted-foreground">
                    No tissues found. Click &apos;Add Tissue&apos; to create one.
                  </td>
                </tr>
              ) : (
                tissues.map((tissue) => (
                  <tr key={tissue.tissue_id} className="border-b hover:bg-muted/50">
                    <td className="px-4 py-3 text-sm">{tissue.tissue_id}</td>
                    <td className="px-4 py-3 text-sm font-medium">{tissue.tissue_name}</td>
                    <td className="px-4 py-3 text-sm max-w-md truncate">{tissue.tissue_description}</td>
                    <td className="px-4 py-3 text-sm">{tissue.tissue_density} g/cm³</td>
                    <td className="px-4 py-3 text-sm">
                      <span
                        className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                          tissue.tissue_is_vital === 'Y'
                            ? 'bg-red-100 text-red-700'
                            : 'bg-gray-100 text-gray-700'
                        }`}
                      >
                        {tissue.tissue_is_vital === 'Y' ? 'Yes' : 'No'}
                      </span>
                    </td>
                    {/* <td className="px-4 py-3 text-sm text-right">
                      <Link href={`/tissues/${tissue.tissue_id}`}>
                        <Button variant="outline" size="sm">
                          View
                        </Button>
                      </Link>
                    </td> */}
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {tissues.length > 0 && (
        <div className="mt-4 text-sm text-muted-foreground">
          Total: {tissues.length} tissue{tissues.length !== 1 ? 's' : ''}
        </div>
      )}
    </div>
  );
}
