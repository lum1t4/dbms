'use client';

import { useEffect, useState } from 'react';
import { donorsAPI } from '@/lib/api/donors';
import type { Donor } from '@/types';

export default function DonorsPage() {
  const [donors, setDonors] = useState<Donor[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchDonors() {
      try {
        setLoading(true);
        const data = await donorsAPI.getAll();
        setDonors(data.donors);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch donors:', err);
        setError('Failed to load donors. Please check if the backend is running.');
      } finally {
        setLoading(false);
      }
    }
    fetchDonors();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-lg">Loading donors...</div>
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
          <h1 className="text-3xl font-bold">Donors</h1>
          <p className="text-muted-foreground mt-1">Manage donor information</p>
        </div>
        {/* <Link href="/donors/new">
          <Button>
            <Plus className="h-4 w-4 mr-2" />
            Add Donor
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
                <th className="px-4 py-3 text-left text-sm font-medium">Surname</th>
                <th className="px-4 py-3 text-left text-sm font-medium">Date of Birth</th>
                <th className="px-4 py-3 text-left text-sm font-medium">Sex</th>
                {/* <th className="px-4 py-3 text-right text-sm font-medium">Actions</th> */}
              </tr>
            </thead>
            <tbody>
              {donors.length === 0 ? (
                <tr>
                  <td colSpan={6} className="px-4 py-8 text-center text-muted-foreground">
                    No donors found. Click &apos;Add Donor&apos; to create one.
                  </td>
                </tr>
              ) : (
                donors.map((donor) => (
                  <tr key={donor.donor_id} className="border-b hover:bg-muted/50">
                    <td className="px-4 py-3 text-sm">{donor.donor_id}</td>
                    <td className="px-4 py-3 text-sm">{donor.donor_name}</td>
                    <td className="px-4 py-3 text-sm">{donor.donor_surname}</td>
                    <td className="px-4 py-3 text-sm">{donor.donor_date_of_birth}</td>
                    <td className="px-4 py-3 text-sm">
                      <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-primary/10 text-primary">
                        {donor.donor_sex}
                      </span>
                    </td>
                    {/* <td className="px-4 py-3 text-sm text-right">
                      <Link href={`/donors/${donor.donor_id}`}>
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

      {donors.length > 0 && (
        <div className="mt-4 text-sm text-muted-foreground">
          Total: {donors.length} donor{donors.length !== 1 ? 's' : ''}
        </div>
      )}
    </div>
  );
}
