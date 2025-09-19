'use client'

import { useState } from 'react'
import { getBrowserSupabaseClient } from '@/lib/supabase/client'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [status, setStatus] = useState<'idle' | 'loading' | 'sent' | 'error'>('idle')
  const [feedback, setFeedback] = useState<string | null>(null)

  const handleSendLink = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setStatus('loading')
    setFeedback(null)

    try {
      const supabase = getBrowserSupabaseClient()
      const origin = window.location.origin
      const { error } = await supabase.auth.signInWithOtp({
        email,
        options: {
          emailRedirectTo: `${origin}/auth/callback`
        }
      })

      if (error) {
        throw error
      }

      setStatus('sent')
      setFeedback('Lien magique envoyé ! Vérifiez votre boîte mail pour continuer.')
      setEmail('')
    } catch (error: unknown) {
      console.error(error)
      setStatus('error')
      setFeedback("Impossible d'envoyer le lien. Veuillez réessayer.")
    }
  }

  return (
    <section className="flex flex-1 flex-col justify-center gap-6">
      <div className="space-y-2 text-center">
        <h1 className="text-3xl font-semibold text-white">Connexion</h1>
        <p className="text-sm text-slate-300">
          Recevez un lien sécurisé par email pour accéder à votre tableau de bord.
        </p>
      </div>
      <form onSubmit={handleSendLink} className="space-y-4">
        <label className="block text-left text-sm font-medium text-slate-200" htmlFor="email">
          Adresse email
        </label>
        <input
          id="email"
          name="email"
          type="email"
          required
          placeholder="vous@example.com"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          className="w-full rounded-2xl border border-slate-700 bg-slate-900 px-4 py-3 text-sm text-white placeholder:text-slate-500 focus:border-accent focus:outline-none focus:ring-2 focus:ring-accent/50"
        />
        <button
          type="submit"
          disabled={status === 'loading' || email.trim().length === 0}
          className="mt-2 inline-flex w-full items-center justify-center rounded-full bg-primary px-6 py-3 text-sm font-semibold text-white transition hover:bg-primary/90 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {status === 'loading' ? 'Envoi en cours...' : 'Recevoir le lien'}
        </button>
      </form>
      {feedback && (
        <p
          className={`text-center text-sm ${status === 'error' ? 'text-red-400' : 'text-slate-200'}`}
        >
          {feedback}
        </p>
      )}
    </section>
  )
}
