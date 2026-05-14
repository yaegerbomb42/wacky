import React, { useEffect, useState } from 'react'
import { createRoot } from 'react-dom/client'

function App() {
  const [tasks, setTasks] = useState([])
  const [title, setTitle] = useState('')
  const [prompt, setPrompt] = useState('')

  const load = async () => {
    const r = await fetch('http://localhost:8000/tasks')
    setTasks(await r.json())
  }
  useEffect(() => { load() }, [])

  const submit = async () => {
    await fetch('http://localhost:8000/tasks', {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ title, prompt, autonomy_mode:'SEMI', time_budget_minutes:60, priority:100 })
    })
    setTitle(''); setPrompt(''); load()
  }

  return <div style={{fontFamily:'sans-serif', padding:20}}>
    <h1>Agent O Queue</h1>
    <input placeholder='task title' value={title} onChange={e=>setTitle(e.target.value)} />
    <br/><textarea placeholder='task prompt' value={prompt} onChange={e=>setPrompt(e.target.value)} rows={4} cols={60}/>
    <br/><button onClick={submit}>Submit task</button>
    <h2>Queue</h2>
    <ul>{tasks.map(t => <li key={t.id}>#{t.id} {t.title} — {t.status}</li>)}</ul>
  </div>
}

createRoot(document.getElementById('root')).render(<App />)
