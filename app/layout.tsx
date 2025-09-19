import './globals.css'
import type { Metadata } from 'next'
import type { ReactNode } from 'react'

export const metadata: Metadata = {
  title: 'Respir',
  description: 'Respir – pratiques de respiration et méditation accessibles depuis votre mobile.'
}

export default function RootLayout({
  children
}: Readonly<{
  children: ReactNode
}>) {
  return (
    <html lang="fr">
      <body className="antialiased">
        <div className="mx-auto flex min-h-screen max-w-md flex-col px-4 py-8">
          <header className="mb-8 flex items-center justify-center">
            <span className="rounded-full bg-primary/20 px-4 py-2 text-sm font-semibold text-primary">
              Respir
            </span>
          </header>
          <main className="flex flex-1 flex-col">{children}</main>
        </div>
      </body>
    </html>
  )
}
