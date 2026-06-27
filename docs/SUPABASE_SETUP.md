# Supabase Setup (Quick Guide)

This project can use Supabase for authentication and lightweight DB storage.

Steps to obtain your Project URL and Anon Key

1. Create a Supabase project
   - Go to https://app.supabase.com and sign in or sign up.
   - Create a new project and follow the onboarding steps.

2. Get the Project URL and API keys
   - In your Supabase project, open `Settings → API`.
   - Copy the `Project URL` (example: `https://abcd1234xyz.supabase.co`).
   - Under `Config` you'll find two important keys:
     - `anon` (public) Key — use this in the frontend (public client).
     - `service_role` Key — secret server-side key (do NOT expose in frontend).

3. Configure the backend (server)
   - Open `Backend/.env` (or create it by copying `Backend/.env.example`).
   - Set:
     - `SUPABASE_URL` to the Project URL
     - `SUPABASE_KEY` to the `service_role` key (server-only)
     - Optionally set `SUPABASE_ANON_KEY` for convenience
   - Restart your backend server.

4. Configure the frontend (client)
   - For static pages, add the following meta tags inside the `<head>` of pages that need Supabase client access:

```html
<meta name="supabase-url" content="https://your-project-ref.supabase.co">
<meta name="supabase-anon-key" content="your-anon-key">
<script src="supabase-client.js"></script>
```

   - The project includes `Frontend/public/supabase-client.js` which will load the Supabase JS SDK and initialize `window._supabase`.
   - In client code you can use `window._supabase` to call Supabase APIs, e.g.:

```js
const { data, error } = await window._supabase.auth.signInWithPassword({ email, password });
```

Security notes
- Never expose the `service_role` key in the browser or public repos. Use it only on the backend (`SUPABASE_KEY` in `Backend/.env`).
- Use `anon` key for client-side actions (signup/signin) and server-side checks for protected operations.

Backend integration
- The backend already includes `Backend/supabase_client.py` which will create a Supabase client if `SUPABASE_URL` and `SUPABASE_KEY` are set in the environment.
- Example usage in backend code:

```py
from supabase_client import get_supabase
supabase = get_supabase()
if supabase:
    resp = supabase.table('users').select('*').execute()
```

If you want, I can:
- Add the meta tags to your public HTML templates (e.g., `index.html`) using values from a build-time config.
- Wire frontend authentication flows (sign-up/sign-in) using Supabase.
- Secure backend endpoints to validate Supabase JWTs.

Which of these should I do next?"}]}