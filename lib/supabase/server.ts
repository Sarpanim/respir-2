import { cookies } from 'next/headers'
import { createClient, type Session, type SupabaseClient } from '@supabase/supabase-js'

const getPublicConfig = () => {
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL
  const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY

  if (!supabaseUrl || !supabaseAnonKey) {
    throw new Error('Supabase public environment variables are not configured')
  }

  return { supabaseUrl, supabaseAnonKey }
}

const getServiceRoleKey = () => {
  const supabaseServiceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY

  if (!supabaseServiceRoleKey) {
    throw new Error('Missing SUPABASE_SERVICE_ROLE_KEY environment variable')
  }

  return supabaseServiceRoleKey
}

export const createServerSupabaseClient = () => {
  const { supabaseUrl, supabaseAnonKey } = getPublicConfig()

  return createClient(supabaseUrl, supabaseAnonKey, {
    auth: {
      persistSession: false,
      autoRefreshToken: false
    }
  })
}

export const createServiceRoleClient = () => {
  const { supabaseUrl } = getPublicConfig()
  const supabaseServiceRoleKey = getServiceRoleKey()

  return createClient(supabaseUrl, supabaseServiceRoleKey, {
    auth: {
      persistSession: false,
      autoRefreshToken: false
    }
  })
}

export const getSessionFromCookies = async (): Promise<
  | {
      supabase: SupabaseClient
      session: Session
    }
  | null
> => {
  const cookieStore = cookies()
  const accessToken = cookieStore.get('sb-access-token')?.value
  const refreshToken = cookieStore.get('sb-refresh-token')?.value

  if (!accessToken || !refreshToken) {
    return null
  }

  const supabase = createServerSupabaseClient()
  const { data, error } = await supabase.auth.setSession({
    access_token: accessToken,
    refresh_token: refreshToken
  })

  if (error || !data.session) {
    return null
  }

  const { data: userData, error: userError } = await supabase.auth.getUser()

  if (userError || !userData.user) {
    return null
  }

  return { supabase, session: data.session }
}
