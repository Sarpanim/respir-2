import Link from 'next/link'

export default function HomePage() {
  return (
    <section className="flex flex-1 flex-col justify-between gap-12">
      <div className="space-y-4 text-center">
        <h1 className="text-3xl font-bold text-white sm:text-4xl">
          Respirez, détendez-vous, progressez
        </h1>
        <p className="text-sm text-slate-300 sm:text-base">
          Des séances guidées, des ambiances adaptées à votre humeur et un suivi de progression
          clair. Tout depuis votre mobile.
        </p>
      </div>
      <div className="space-y-6">
        <div className="rounded-3xl bg-white/5 p-6 text-left shadow-lg">
          <p className="text-base font-medium text-white">
            Routines express
            <span className="ml-2 inline-flex items-center rounded-full bg-accent/20 px-2 py-1 text-xs font-semibold text-accent">
              5-10 min
            </span>
          </p>
          <p className="mt-2 text-sm text-slate-300">
            Reprenez le contrôle en quelques minutes avec des respirations guidées.
          </p>
        </div>
        <div className="rounded-3xl bg-white/5 p-6 text-left shadow-lg">
          <p className="text-base font-medium text-white">Ambiances immersives</p>
          <p className="mt-2 text-sm text-slate-300">
            Choisissez la playlist sonore qui vous inspire : forêt, océan, minimalisme.
          </p>
        </div>
      </div>
      <div className="space-y-3 text-center">
        <Link
          href="/login"
          className="inline-flex w-full items-center justify-center rounded-full bg-accent px-6 py-3 text-base font-semibold text-slate-950 transition hover:bg-accent/90"
        >
          Accéder à mon espace
        </Link>
        <p className="text-xs text-slate-400">
          Pas de compte ? Entrez votre email pour recevoir un lien magique et commencer.
        </p>
      </div>
    </section>
  )
}
