'use client';

import { useState } from 'react';
import { operationsAPI } from '@/lib/api/operations';
import type {
  TissuesByDensityResponse,
  CureDetail,
  DonorsVitalDiseaseResponse,
  TopResearchersResponse,
} from '@/types';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

export default function OperationsPage() {
  const [activeTab, setActiveTab] = useState<'op2' | 'op3' | 'op4' | 'op5'>('op2');

  // OP2 State
  const [maxDensity, setMaxDensity] = useState('1.0');
  const [op2Result, setOp2Result] = useState<TissuesByDensityResponse | null>(null);
  const [op2Loading, setOp2Loading] = useState(false);

  // OP3 State
  const [cureId, setCureId] = useState('1');
  const [op3Result, setOp3Result] = useState<CureDetail | null>(null);
  const [op3Loading, setOp3Loading] = useState(false);

  // OP4 State
  const [diseaseId, setDiseaseId] = useState('2');
  const [op4Result, setOp4Result] = useState<DonorsVitalDiseaseResponse | null>(null);
  const [op4Loading, setOp4Loading] = useState(false);

  // OP5 State
  const [quality, setQuality] = useState<'top' | 'middle' | 'low'>('top');
  const [op5Result, setOp5Result] = useState<TopResearchersResponse | null>(null);
  const [op5Loading, setOp5Loading] = useState(false);

  const handleOp2 = async () => {
    setOp2Loading(true);
    try {
      const result = await operationsAPI.getTissuesByDensity(parseFloat(maxDensity));
      setOp2Result(result);
    } catch (error) {
      console.error('OP2 Error:', error);
    } finally {
      setOp2Loading(false);
    }
  };

  const handleOp3 = async () => {
    setOp3Loading(true);
    try {
      const result = await operationsAPI.getCureDetails(parseInt(cureId));
      setOp3Result(result);
    } catch (error) {
      console.error('OP3 Error:', error);
    } finally {
      setOp3Loading(false);
    }
  };

  const handleOp4 = async () => {
    setOp4Loading(true);
    try {
      const result = await operationsAPI.getDonorsVitalDisease(parseInt(diseaseId));
      setOp4Result(result);
    } catch (error) {
      console.error('OP4 Error:', error);
    } finally {
      setOp4Loading(false);
    }
  };

  const handleOp5 = async () => {
    setOp5Loading(true);
    try {
      const result = await operationsAPI.getTopResearchersSuggestions(quality);
      setOp5Result(result);
    } catch (error) {
      console.error('OP5 Error:', error);
    } finally {
      setOp5Loading(false);
    }
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Operations</h1>

      {/* Tabs */}
      <div className="border-b mb-6">
        <div className="flex gap-4">
          {[
            { id: 'op2', label: 'OP2: Tissues by Density' },
            { id: 'op3', label: 'OP3: Cure Details' },
            { id: 'op4', label: 'OP4: Donors with Disease' },
            { id: 'op5', label: 'OP5: Top Researchers' },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as 'op2' | 'op3' | 'op4' | 'op5')}
              className={`px-4 py-2 border-b-2 transition-colors ${
                activeTab === tab.id
                  ? 'border-primary text-primary font-medium'
                  : 'border-transparent text-muted-foreground hover:text-foreground'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* OP2: Tissues by Density */}
      {activeTab === 'op2' && (
        <div className="space-y-4">
          <div className="bg-card p-6 rounded-lg border">
            <h2 className="text-xl font-semibold mb-4">Get Tissues Below Density Threshold</h2>
            <div className="flex gap-4 items-end">
              <div className="flex-1 max-w-xs">
                <Label htmlFor="maxDensity">Maximum Density (g/cm³)</Label>
                <Input
                  id="maxDensity"
                  type="number"
                  step="0.1"
                  value={maxDensity}
                  onChange={(e) => setMaxDensity(e.target.value)}
                />
              </div>
              <Button onClick={handleOp2} disabled={op2Loading}>
                {op2Loading ? 'Loading...' : 'Search'}
              </Button>
            </div>
          </div>

          {op2Result && (
            <div className="bg-card p-6 rounded-lg border">
              <h3 className="font-semibold mb-2">
                Results: {op2Result.count} tissue{op2Result.count !== 1 ? 's' : ''} below {op2Result.threshold} g/cm³
              </h3>
              <div className="overflow-x-auto">
                <table className="w-full mt-4">
                  <thead className="border-b">
                    <tr>
                      <th className="px-4 py-2 text-left">ID</th>
                      <th className="px-4 py-2 text-left">Name</th>
                      <th className="px-4 py-2 text-left">Density</th>
                      <th className="px-4 py-2 text-left">Vital</th>
                    </tr>
                  </thead>
                  <tbody>
                    {op2Result.tissues.map((tissue) => (
                      <tr key={tissue.tissue_id} className="border-b">
                        <td className="px-4 py-2">{tissue.tissue_id}</td>
                        <td className="px-4 py-2">{tissue.tissue_name}</td>
                        <td className="px-4 py-2">{tissue.tissue_density}</td>
                        <td className="px-4 py-2">{tissue.tissue_is_vital}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}

      {/* OP3: Cure Details */}
      {activeTab === 'op3' && (
        <div className="space-y-4">
          <div className="bg-card p-6 rounded-lg border">
            <h2 className="text-xl font-semibold mb-4">Get Cure Details with Drugs and Allergies</h2>
            <div className="flex gap-4 items-end">
              <div className="flex-1 max-w-xs">
                <Label htmlFor="cureId">Cure ID</Label>
                <Input
                  id="cureId"
                  type="number"
                  value={cureId}
                  onChange={(e) => setCureId(e.target.value)}
                />
              </div>
              <Button onClick={handleOp3} disabled={op3Loading}>
                {op3Loading ? 'Loading...' : 'Get Details'}
              </Button>
            </div>
          </div>

          {op3Result && (
            <div className="bg-card p-6 rounded-lg border">
              <h3 className="font-semibold mb-4">Cure #{op3Result.cure_id} Details</h3>

              <div className="mb-4">
                <h4 className="font-medium mb-2">Drugs:</h4>
                {op3Result.drugs.map((drug) => (
                  <div key={drug.drug_id} className="ml-4 mb-2">
                    <div className="font-medium">{drug.drug_name}</div>
                    <div className="text-sm text-muted-foreground">{drug.drug_description}</div>
                  </div>
                ))}
              </div>

              <div>
                <h4 className="font-medium mb-2">All Allergies:</h4>
                <div className="flex flex-wrap gap-2">
                  {op3Result.all_allergies.map((allergy, idx) => (
                    <span
                      key={idx}
                      className="px-3 py-1 bg-orange-100 text-orange-700 rounded-full text-sm"
                    >
                      {allergy}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* OP4: Donors with Disease */}
      {activeTab === 'op4' && (
        <div className="space-y-4">
          <div className="bg-card p-6 rounded-lg border">
            <h2 className="text-xl font-semibold mb-4">Donors with Vital Tissue Disease</h2>
            <div className="flex gap-4 items-end">
              <div className="flex-1 max-w-xs">
                <Label htmlFor="diseaseId">Disease ID</Label>
                <Input
                  id="diseaseId"
                  type="number"
                  value={diseaseId}
                  onChange={(e) => setDiseaseId(e.target.value)}
                />
              </div>
              <Button onClick={handleOp4} disabled={op4Loading}>
                {op4Loading ? 'Loading...' : 'Search'}
              </Button>
            </div>
          </div>

          {op4Result && (
            <div className="bg-card p-6 rounded-lg border">
              <h3 className="font-semibold mb-2">
                Disease: {op4Result.disease_name || `ID ${op4Result.disease_id}`}
              </h3>
              <p className="text-sm text-muted-foreground mb-4">
                Found {op4Result.donors.length} donor{op4Result.donors.length !== 1 ? 's' : ''}
              </p>

              {op4Result.donors.map((donor) => (
                <div key={donor.donor_id} className="mb-4 p-4 border rounded">
                  <div className="font-medium">
                    {donor.donor_name} {donor.donor_surname}
                  </div>
                  <div className="text-sm text-muted-foreground">
                    ID: {donor.donor_id} | DOB: {donor.donor_date_of_birth} | Sex: {donor.donor_sex}
                  </div>
                  <div className="mt-2">
                    <span className="text-sm font-medium">Affected Vital Tissues:</span>
                    {donor.affected_vital_tissues.map((tissue) => (
                      <span
                        key={tissue.tissue_id}
                        className="ml-2 px-2 py-1 bg-red-100 text-red-700 rounded text-xs"
                      >
                        {tissue.tissue_name}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* OP5: Top Researchers */}
      {activeTab === 'op5' && (
        <div className="space-y-4">
          <div className="bg-card p-6 rounded-lg border">
            <h2 className="text-xl font-semibold mb-4">Top Researchers Suggestions</h2>
            <div className="flex gap-4 items-end">
              <div className="flex-1 max-w-xs">
                <Label htmlFor="quality">Journal Quality</Label>
                <select
                  id="quality"
                  value={quality}
                  onChange={(e) => setQuality(e.target.value as 'top' | 'middle' | 'low')}
                  className="w-full px-3 py-2 border rounded"
                >
                  <option value="top">Top</option>
                  <option value="middle">Middle</option>
                  <option value="low">Low</option>
                </select>
              </div>
              <Button onClick={handleOp5} disabled={op5Loading}>
                {op5Loading ? 'Loading...' : 'Search'}
              </Button>
            </div>
          </div>

          {op5Result && (
            <div className="bg-card p-6 rounded-lg border">
              <h3 className="font-semibold mb-4">
                {op5Result.researchers.length} researcher{op5Result.researchers.length !== 1 ? 's' : ''} with {quality}{' '}
                quality publications
              </h3>

              {op5Result.researchers.map((researcher) => (
                <div key={researcher.researcher_id} className="mb-6 p-4 border rounded">
                  <div className="font-medium text-lg">
                    {researcher.researcher_name} {researcher.researcher_surname}
                  </div>
                  <div className="text-sm text-muted-foreground mb-2">
                    {researcher.researcher_email} | {researcher.researcher_institution}
                  </div>

                  <div className="mt-3">
                    <div className="text-sm font-medium mb-1">Publications:</div>
                    {researcher.top_publications.map((pub) => (
                      <div key={pub.publication_doi} className="text-sm ml-4 mb-1">
                        • {pub.publication_title} ({pub.publication_journal})
                      </div>
                    ))}
                  </div>

                  <div className="mt-3">
                    <div className="text-sm font-medium mb-1">Suggested Future Works:</div>
                    {researcher.suggested_future_works.map((fw) => (
                      <div key={fw.future_work_id} className="text-sm ml-4 mb-1">
                        • {fw.future_work_description}
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
