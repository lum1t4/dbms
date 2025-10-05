'use client';

import { useEffect, useState } from 'react';
import { drugsAPI } from '@/lib/api/drugs';
import type { Drug } from '@/types';

export default function DrugsPage() {
  const [drugs, setDrugs] = useState<Drug[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchDrugs() {
      try {
        setLoading(true);
        const data = await drugsAPI.getAll();
        setDrugs(data.drugs);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch drugs:', err);
        setError('Failed to load drugs. Please check if the backend is running.');
      } finally {
        setLoading(false);
      }
    }
    fetchDrugs();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-lg">Loading drugs...</div>
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
          <h1 className="text-3xl font-bold">Drugs</h1>
          <p className="text-muted-foreground mt-1">Manage pharmaceutical information</p>
        </div>
        {/* <Link href="/drugs/new">
          <Button>
            <Plus className="h-4 w-4 mr-2" />
            Add Drug
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
                <th className="px-4 py-3 text-left text-sm font-medium">Allergies</th>
                {/* <th className="px-4 py-3 text-right text-sm font-medium">Actions</th> */}
              </tr>
            </thead>
            <tbody>
              {drugs.length === 0 ? (
                <tr>
                  <td colSpan={5} className="px-4 py-8 text-center text-muted-foreground">
                    No drugs found. Click &apos;Add Drug&apos; to create one.
                  </td>
                </tr>
              ) : (
                drugs.map((drug) => (
                  <tr key={drug.drug_id} className="border-b hover:bg-muted/50">
                    <td className="px-4 py-3 text-sm">{drug.drug_id}</td>
                    <td className="px-4 py-3 text-sm font-medium">{drug.drug_name}</td>
                    <td className="px-4 py-3 text-sm max-w-md truncate">{drug.drug_description}</td>
                    <td className="px-4 py-3 text-sm">
                      {drug.drug_allergies.length > 0 ? (
                        <div className="flex flex-wrap gap-1">
                          {drug.drug_allergies.slice(0, 2).map((allergy, idx) => (
                            <span
                              key={idx}
                              className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-orange-100 text-orange-700"
                            >
                              {allergy}
                            </span>
                          ))}
                          {drug.drug_allergies.length > 2 && (
                            <span className="text-xs text-muted-foreground">
                              +{drug.drug_allergies.length - 2} more
                            </span>
                          )}
                        </div>
                      ) : (
                        <span className="text-muted-foreground text-sm">None</span>
                      )}
                    </td>
                    {/* <td className="px-4 py-3 text-sm text-right">
                      <Link href={`/drugs/${drug.drug_id}`}>
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

      {drugs.length > 0 && (
        <div className="mt-4 text-sm text-muted-foreground">
          Total: {drugs.length} drug{drugs.length !== 1 ? 's' : ''}
        </div>
      )}
    </div>
  );
}
