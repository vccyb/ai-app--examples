export type SSEPostOptions = {
  params: Record<string, any>
  signal: AbortSignal
}

export async function ssePost<T>(path: string, options: SSEPostOptions) {
  const { params, signal } = options

  return new Promise<AsyncGenerator<T>>((resolve, reject) => {
    let resolvers: PromiseWithResolvers<T | null>

    const generator = async function* () {
      while (true) {
        resolvers = Promise.withResolvers<T | null>()
        const result = await resolvers.promise
        if (result === null) break
        yield result
      }
    }

    fetch(path, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(params),
      signal,
    })
      .then(async (res) => {
        if (!res.ok) {
          const text = (await res.text()) || res.statusText
          throw new Error(text)
        }
        resolve(generator())
        return res.body
      })
      .then(async (body) => {
        if (!body) throw new Error('no body present')
        const decoder = new TextDecoder()
        for await (const chunk of body) {
          const lines = decoder
            .decode(chunk, { stream: true })
            .split('\n')
            .map((line) => line.trim())
            .filter(Boolean)
          for (const line of lines) {
            const colonIndex = line.indexOf(':')
            if (colonIndex === -1) continue
            const key = line.slice(0, colonIndex).trim()
            const value = line.slice(colonIndex + 1).trim()
            setTimeout(() => {
              if (key === 'data' && value) resolvers?.resolve(JSON.parse(value))
              if (key === 'event' && value === 'close') resolvers?.resolve(null)
            })
          }
        }
      })
      .catch((err) => {
        resolvers?.reject(err)
        reject(err)
      })
  })
}