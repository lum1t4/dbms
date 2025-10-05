# WHO Frontend Setup Guide

## Initial Setup

### 1. Install Dependencies

```bash
cd frontend
bun install
```

### 2. Install shadcn/ui Components

The project uses shadcn/ui components. Install the required components:

```bash
npx shadcn@latest add button
npx shadcn@latest add card
npx shadcn@latest add input
npx shadcn@latest add label
npx shadcn@latest add table
npx shadcn@latest add dialog
npx shadcn@latest add select
npx shadcn@latest add tabs
npx shadcn@latest add badge
npx shadcn@latest add alert
npx shadcn@latest add form
npx shadcn@latest add separator
```

### 3. Environment Variables

Create `.env.local` if it doesn't exist:

```bash
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

### 4. Run Development Server

```bash
bun run dev
```

Open [http://localhost:3000](http://localhost:3000)

---

## Project Structure

```
frontend/
├── app/                    # Next.js app router pages
│   ├── layout.tsx         # Root layout with navigation
│   ├── page.tsx           # Dashboard (home)
│   ├── donors/            # Donors CRUD pages
│   ├── tissues/           # Tissues CRUD pages
│   ├── drugs/             # Drugs CRUD pages
│   └── operations/        # Operations page
├── components/
│   ├── ui/                # shadcn components (auto-generated)
│   ├── layout/
│   │   └── nav.tsx       # Navigation sidebar
│   ├── donors/           # Donor-specific components
│   ├── tissues/          # Tissue-specific components
│   ├── drugs/            # Drug-specific components
│   └── operations/       # Operation components
├── lib/
│   ├── api/              # API client
│   │   ├── client.ts    # Axios configuration
│   │   ├── donors.ts    # Donor API methods
│   │   ├── tissues.ts   # Tissue API methods
│   │   ├── drugs.ts     # Drug API methods
│   │   └── operations.ts # Operations API methods
│   └── utils.ts          # Utility functions
└── types/
    └── index.ts          # TypeScript types
```

---

## Implementation Status

### ✅ Completed
- [x] Project setup and configuration
- [x] TypeScript types for all entities
- [x] API client for all endpoints
- [x] Layout with navigation sidebar
- [x] Environment configuration

### 🚧 To Implement

#### Pages (in order):
1. **Dashboard** (`app/page.tsx`)
   - Quick stats cards (total donors, tissues, drugs)
   - Recent activities
   - Quick links to operations

2. **Donors CRUD** (`app/donors/`)
   - `page.tsx` - List all donors with search/filter
   - `new/page.tsx` - Create new donor form
   - `[id]/page.tsx` - View/Edit donor details

3. **Tissues CRUD** (`app/tissues/`)
   - `page.tsx` - List all tissues
   - `new/page.tsx` - Create tissue (Operation 1)
   - `[id]/page.tsx` - View/Edit tissue

4. **Drugs CRUD** (`app/drugs/`)
   - `page.tsx` - List all drugs
   - `new/page.tsx` - Create drug with allergies
   - `[id]/page.tsx` - View/Edit drug

5. **Operations Page** (`app/operations/page.tsx`)
   - Tabbed interface with 5 operations
   - OP2: Tissues by density
   - OP3: Cure details
   - OP4: Donors with vital disease
   - OP5: Top researchers

---

## Implementation Guide

### Creating a CRUD Page (Example: Donors)

#### 1. List Page (`app/donors/page.tsx`)

```tsx
'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { donorsAPI } from '@/lib/api/donors';
import type { Donor } from '@/types';
import { Button } from '@/components/ui/button';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';

export default function DonorsPage() {
  const [donors, setDonors] = useState<Donor[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchDonors() {
      try {
        const data = await donorsAPI.getAll();
        setDonors(data.donors);
      } catch (error) {
        console.error('Failed to fetch donors:', error);
      } finally {
        setLoading(false);
      }
    }
    fetchDonors();
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Donors</h1>
        <Link href="/donors/new">
          <Button>Add Donor</Button>
        </Link>
      </div>

      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>ID</TableHead>
            <TableHead>Name</TableHead>
            <TableHead>Surname</TableHead>
            <TableHead>Date of Birth</TableHead>
            <TableHead>Sex</TableHead>
            <TableHead>Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {donors.map((donor) => (
            <TableRow key={donor.donor_id}>
              <TableCell>{donor.donor_id}</TableCell>
              <TableCell>{donor.donor_name}</TableCell>
              <TableCell>{donor.donor_surname}</TableCell>
              <TableCell>{donor.donor_date_of_birth}</TableCell>
              <TableCell>{donor.donor_sex}</TableCell>
              <TableCell>
                <Link href={`/donors/${donor.donor_id}`}>
                  <Button variant="outline" size="sm">View</Button>
                </Link>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
```

#### 2. Create Page (`app/donors/new/page.tsx`)

```tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { donorsAPI } from '@/lib/api/donors';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

export default function NewDonorPage() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    donor_name: '',
    donor_surname: '',
    donor_date_of_birth: '',
    donor_sex: 'M' as 'M' | 'F' | 'X',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await donorsAPI.create(formData);
      router.push('/donors');
    } catch (error) {
      console.error('Failed to create donor:', error);
    }
  };

  return (
    <div className="max-w-2xl">
      <h1 className="text-3xl font-bold mb-6">Add New Donor</h1>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <Label htmlFor="name">Name</Label>
          <Input
            id="name"
            value={formData.donor_name}
            onChange={(e) => setFormData({ ...formData, donor_name: e.target.value })}
            required
          />
        </div>

        <div>
          <Label htmlFor="surname">Surname</Label>
          <Input
            id="surname"
            value={formData.donor_surname}
            onChange={(e) => setFormData({ ...formData, donor_surname: e.target.value })}
            required
          />
        </div>

        <div>
          <Label htmlFor="dob">Date of Birth</Label>
          <Input
            id="dob"
            type="date"
            value={formData.donor_date_of_birth}
            onChange={(e) => setFormData({ ...formData, donor_date_of_birth: e.target.value })}
            required
          />
        </div>

        <div>
          <Label htmlFor="sex">Sex</Label>
          <Select
            value={formData.donor_sex}
            onValueChange={(value: 'M' | 'F' | 'X') => setFormData({ ...formData, donor_sex: value })}
          >
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="M">Male</SelectItem>
              <SelectItem value="F">Female</SelectItem>
              <SelectItem value="X">Other</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="flex gap-4">
          <Button type="submit">Create Donor</Button>
          <Button type="button" variant="outline" onClick={() => router.back()}>
            Cancel
          </Button>
        </div>
      </form>
    </div>
  );
}
```

#### 3. Detail/Edit Page (`app/donors/[id]/page.tsx`)

Similar structure to the new page, but:
- Fetch donor data on mount
- Pre-fill form with existing data
- Use `update` instead of `create` API method
- Add delete button with confirmation dialog

---

## Operations Page Structure

The operations page uses tabs for each operation:

```tsx
'use client';

import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
// Import operation components

export default function OperationsPage() {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Operations</h1>

      <Tabs defaultValue="op2">
        <TabsList>
          <TabsTrigger value="op2">Tissues by Density</TabsTrigger>
          <TabsTrigger value="op3">Cure Details</TabsTrigger>
          <TabsTrigger value="op4">Donors with Disease</TabsTrigger>
          <TabsTrigger value="op5">Top Researchers</TabsTrigger>
        </TabsList>

        <TabsContent value="op2">
          {/* OP2 Component */}
        </TabsContent>

        <TabsContent value="op3">
          {/* OP3 Component */}
        </TabsContent>

        <TabsContent value="op4">
          {/* OP4 Component */}
        </TabsContent>

        <TabsContent value="op5">
          {/* OP5 Component */}
        </TabsContent>
      </Tabs>
    </div>
  );
}
```

---

## Development Tips

### 1. Error Handling

Always wrap API calls in try-catch:

```tsx
try {
  const data = await donorsAPI.getAll();
  setDonors(data.donors);
} catch (error) {
  if (axios.isAxiosError(error)) {
    // Handle API error
    console.error(error.response?.data);
  }
}
```

### 2. Loading States

Use loading states for better UX:

```tsx
const [loading, setLoading] = useState(true);

if (loading) return <div>Loading...</div>;
```

### 3. Form Validation

Use zod for form validation:

```tsx
import { z } from 'zod';

const donorSchema = z.object({
  donor_name: z.string().min(1).max(100),
  donor_surname: z.string().min(1).max(100),
  donor_date_of_birth: z.string(),
  donor_sex: z.enum(['M', 'F', 'X']),
});
```

---

## Next Steps

1. **Install shadcn components** (listed above)
2. **Implement Dashboard** - Start with simple stats
3. **Implement Donors CRUD** - Use examples above
4. **Copy pattern for Tissues** - Similar to Donors but with density field
5. **Copy pattern for Drugs** - Add dynamic array for allergies
6. **Build Operations page** - Use tabs and API calls

---

## Backend Connection

Ensure the FastAPI backend is running:

```bash
cd ../backend
uvicorn main:app --reload
```

The frontend will connect to `http://127.0.0.1:8000` by default.
