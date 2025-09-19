import { type NextRequest, NextResponse } from 'next/server'
import { createServerSupabaseClient } from '@/lib/supabase/server'

export async function GET(request: NextRequest) {
  const { searchParams, origin } = new URL(request.url)
  const code = searchParams.get('code')
  const rawNext = searchParams.get('next')
  const nextPath = rawNext && rawNext.startsWith('/') ? rawNext : '/dashboard'

  if (!code) {
    return NextResponse.redirect(`${origin}/login?error=missing_code`)
  }

  const supabase = createServerSupabaseClient()
  const { data, error } = await supabase.auth.exchangeCodeForSession(code)

  if (error || !data.session) {
    return NextResponse.redirect(`${origin}/login?error=auth_failed`)
  }

  const response = NextResponse.redirect(`${origin}${nextPath}`)
  const isProduction = process.env.NODE_ENV === 'production'
  const { session } = data

  response.cookies.set('sb-access-token', session.access_token, {
    httpOnly: true,
    path: '/',
    secure: isProduction,
    sameSite: 'lax',
    maxAge: session.expires_in ?? 3600
  })

  if (session.refresh_token) {
    response.cookies.set('sb-refresh-token', session.refresh_token, {
      httpOnly: true,
      path: '/',
      secure: isProduction,
      sameSite: 'lax',
      maxAge: 60 * 60 * 24 * 30
    })
  }

  return response
}
