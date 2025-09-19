import { type NextRequest, NextResponse } from 'next/server'
import { createServerSupabaseClient } from '@/lib/supabase/server'

export async function POST(request: NextRequest) {
  const response = NextResponse.redirect(new URL('/login', request.url))
  const accessToken = request.cookies.get('sb-access-token')?.value
  const refreshToken = request.cookies.get('sb-refresh-token')?.value

  if (accessToken && refreshToken) {
    const supabase = createServerSupabaseClient()
    await supabase.auth.setSession({
      access_token: accessToken,
      refresh_token: refreshToken
    })
    await supabase.auth.signOut()
  }

  response.cookies.delete('sb-access-token')
  response.cookies.delete('sb-refresh-token')

  return response
}
