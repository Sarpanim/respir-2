import Link from 'next/link'
import { redirect } from 'next/navigation'
import { getSessionFromCookies } from '@/lib/supabase/server'

export default async function DashboardPage() {
  const sessionData = await getSessionFromCookies()

  if (!sessionData) {
    redirect('/login')
  }

  const {
    session: { user }
  } = sessionData
  const userEmail = user.email ?? 'Utilisateur'

  return (
    <section className="flex flex-1 flex-col gap-6">
      <div className="space-y-1">
        <p className="text-sm text-slate-400">Bienvenue</p>
        <h1 className="text-3xl font-semibold text-white">{userEmail}</h1>
      </div>
      <div className="space-y-4">
        <div className="rounded-3xl bg-white/5 p-6 shadow-lg">
          <h2 className="text-lg font-semibold text-white">Votre prochaine séance</h2>
          <p className="mt-2 text-sm text-slate-300">
            Reprenez là où vous en étiez. Votre progression se synchronise automatiquement.
          </p>
          <div className="mt-4 flex items-center justify-between rounded-2xl bg-slate-900/60 px-4 py-3">
            <span className="text-sm text-slate-200">Respiration consciente</span>
            <span className="text-xs text-slate-400">12 min restantes</span>
          </div>
        </div>
        <div className="rounded-3xl bg-white/5 p-6 shadow-lg">
          <h2 className="text-lg font-semibold text-white">Ambiances favorites</h2>
          <ul className="mt-3 space-y-2 text-sm text-slate-300">
            <li>🌊 Océan profond</li>
            <li>🌲 Forêt matinale</li>
            <li>🎧 Minimalisme électronique</li>
          </ul>
        </div>
      </div>
      <form action="/logout" method="post" className="mt-auto text-center">
        <button
          type="submit"
          className="inline-flex w-full items-center justify-center rounded-full border border-slate-700 px-6 py-3 text-sm font-semibold text-slate-200 transition hover:border-accent hover:text-white"
        >
          Se déconnecter
        </button>
      </form>
      <p className="text-center text-xs text-slate-500">
        Besoin d’aide ? <Link href="mailto:support@respir.app">support@respir.app</Link>
      </p>
    </section>
  )
}
