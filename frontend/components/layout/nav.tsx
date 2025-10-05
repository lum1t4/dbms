'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Home, Users, ActivitySquare, Pill, FlaskConical } from 'lucide-react';
import { cn } from '@/lib/utils';

const navItems = [
  { href: '/', label: 'Dashboard', icon: Home },
  { href: '/donors', label: 'Donors', icon: Users },
  { href: '/tissues', label: 'Tissues', icon: ActivitySquare },
  { href: '/drugs', label: 'Drugs', icon: Pill },
  { href: '/operations', label: 'Operations', icon: FlaskConical },
];

export function Nav() {
  const pathname = usePathname();

  return (
    <nav className="w-64 bg-card border-r min-h-screen p-4">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-primary">WHO Database</h1>
        <p className="text-sm text-muted-foreground">Disease Monitoring System</p>
      </div>
      <ul className="space-y-2">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href || pathname.startsWith(item.href + '/');
          return (
            <li key={item.href}>
              <Link
                href={item.href}
                className={cn(
                  'flex items-center gap-3 px-4 py-2 rounded-md transition-colors',
                  isActive
                    ? 'bg-primary text-primary-foreground'
                    : 'hover:bg-accent hover:text-accent-foreground'
                )}
              >
                <Icon className="h-5 w-5" />
                <span>{item.label}</span>
              </Link>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}
