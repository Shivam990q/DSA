# ⚛️ 06 — Forms & Controlled Components

> *"A form is just state with a face. Decide who owns each value — React or the DOM — and most form 'mysteries' evaporate. Controlled forms make React the single source of truth; embrace that and you can validate, transform, and reason about every keystroke."*

**Prev:** [`05-Context-And-State-Management.md`](./05-Context-And-State-Management.md) · **Next:** [`07-Data-Fetching-And-Effects.md`](./07-Data-Fetching-And-Effects.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. THE CENTRAL QUESTION: WHO OWNS THE VALUE?

Every form input holds a value. The defining question in React forms is **where that value lives**:

- **Controlled** — React state owns the value. The input displays state; every change updates state. React is the single source of truth.
- **Uncontrolled** — the DOM owns the value. React reads it only when needed (e.g. on submit), via a ref.

```
CONTROLLED                                  UNCONTROLLED
  state ──value──► <input>                    <input> (DOM holds value)
    ▲                 │                          │
    └──onChange───────┘                          └── ref.current.value (read on demand)
  React is source of truth                    DOM is source of truth
```

Controlled is the default recommendation: it lets you validate live, disable the submit button, format input, and keep everything in sync. Uncontrolled is handy for simple cases, file inputs, and integrating non-React code.

---

## II. CONTROLLED INPUTS — THE CORE PATTERN

A controlled input needs two things: a `value` bound to state, and an `onChange` that updates that state. Miss either and you get a bug.

```jsx
import { useState } from 'react';

function NameForm() {
  const [name, setName] = useState('');     // React owns the value

  return (
    <input
      value={name}                          // input always reflects state
      onChange={(e) => setName(e.target.value)}  // every keystroke updates state
    />
  );
}
```

The flow on each keystroke: you type → `onChange` fires → `setName` updates state → component re-renders → `value={name}` shows the new state. React is in the loop for every character.

> **Gotcha — `value` without `onChange` = a read-only input.** `<input value={name} />` with no `onChange` locks the field: React keeps forcing it back to `name`, so typing does nothing. React even warns you. Either add `onChange`, or use `defaultValue` (uncontrolled), or `readOnly` if that's truly intended.

> **Gotcha — `value={undefined}` flips controlled ↔ uncontrolled.** If state starts as `undefined`, React treats the input as uncontrolled, then "switches to controlled" when you set a string — and warns. **Always initialize controlled state to a defined value** (`''` for text, `false` for checkbox), never `undefined`/`null`.

---

## III. EVERY INPUT TYPE, CONTROLLED

Different inputs bind their value differently. Memorize these — they're the ones interviews and real forms hit.

```jsx
function AllInputs() {
  const [text, setText]       = useState('');
  const [bio, setBio]         = useState('');
  const [country, setCountry] = useState('us');
  const [agree, setAgree]     = useState(false);
  const [plan, setPlan]       = useState('free');
  const [colors, setColors]   = useState([]);     // multi-select via checkboxes

  function toggleColor(color) {
    setColors((prev) =>
      prev.includes(color) ? prev.filter((c) => c !== color) : [...prev, color]
    );
  }

  return (
    <form>
      {/* text / email / password / number — bind value */}
      <input type="text" value={text} onChange={(e) => setText(e.target.value)} />

      {/* textarea — value as a prop, NOT children (unlike HTML) */}
      <textarea value={bio} onChange={(e) => setBio(e.target.value)} />

      {/* select — value on the <select>, NOT `selected` on <option> */}
      <select value={country} onChange={(e) => setCountry(e.target.value)}>
        <option value="us">USA</option>
        <option value="in">India</option>
        <option value="uk">UK</option>
      </select>

      {/* checkbox (boolean) — use `checked`, not `value` */}
      <label>
        <input type="checkbox" checked={agree} onChange={(e) => setAgree(e.target.checked)} />
        I agree
      </label>

      {/* radio group — same state, compare value to decide checked */}
      <label><input type="radio" value="free" checked={plan === 'free'}
        onChange={(e) => setPlan(e.target.value)} /> Free</label>
      <label><input type="radio" value="pro" checked={plan === 'pro'}
        onChange={(e) => setPlan(e.target.value)} /> Pro</label>

      {/* checkbox group → array state */}
      {['red', 'green', 'blue'].map((c) => (
        <label key={c}>
          <input type="checkbox" checked={colors.includes(c)} onChange={() => toggleColor(c)} />
          {c}
        </label>
      ))}
    </form>
  );
}
```

| Input | Bind with | Read change from |
|-------|-----------|------------------|
| text / email / password / number | `value` | `e.target.value` |
| `<textarea>` | `value` (prop, not children) | `e.target.value` |
| `<select>` | `value` on select | `e.target.value` |
| checkbox (single) | `checked` | `e.target.checked` |
| radio group | `checked={state === v}` | `e.target.value` |
| `<select multiple>` | `value={array}` | `[...e.target.selectedOptions].map(o => o.value)` |

> **Gotcha — `<textarea>` and `<select>` differ from HTML.** In HTML, a textarea's text is its children and a select uses `<option selected>`. In React, **both use the `value` prop** on the parent element. Forgetting this is a classic source of "why won't my select update."

> **Gotcha — number inputs return strings.** `e.target.value` is always a **string**, even for `type="number"`. Convert when you need a number: `Number(e.target.value)` or `e.target.valueAsNumber`. Doing math on the raw string gives `"5"+1 === "51"`.

---

## IV. MULTI-FIELD FORMS — ONE STATE OBJECT, ONE HANDLER

A form with ten fields doesn't need ten `useState`s and ten handlers. Hold the whole form in one object and write a single generic handler keyed by the input's `name`.

```jsx
function SignupForm() {
  const [form, setForm] = useState({
    username: '',
    email: '',
    password: '',
    newsletter: false,
  });

  // ONE handler for all fields. Uses the input's `name` as the key,
  // and reads `checked` for checkboxes, `value` for everything else.
  function handleChange(e) {
    const { name, value, type, checked } = e.target;
    setForm((prev) => ({
      ...prev,                                   // keep other fields
      [name]: type === 'checkbox' ? checked : value,  // computed key + right value
    }));
  }

  function handleSubmit(e) {
    e.preventDefault();
    console.log(form);                            // { username, email, password, newsletter }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input name="username" value={form.username} onChange={handleChange} placeholder="Username" />
      <input name="email"    value={form.email}    onChange={handleChange} placeholder="Email" />
      <input name="password" type="password" value={form.password} onChange={handleChange} />
      <label>
        <input name="newsletter" type="checkbox" checked={form.newsletter} onChange={handleChange} />
        Subscribe
      </label>
      <button type="submit">Sign up</button>
    </form>
  );
}
```

The trick is the **computed property key** `[name]: ...` combined with the input's `name` attribute. Add a field → add one input with a `name`. No new state, no new handler.

> **Gotcha — spread to preserve other fields.** `setForm({ [name]: value })` would *replace* the whole object, wiping every other field. Always `setForm(prev => ({ ...prev, [name]: value }))` so untouched fields survive.

---

## V. VALIDATION — MANUAL FIRST

Validation has two timings: **on submit** (validate everything when they click) and **live/on blur** (validate a field as they leave or type it). Real forms usually combine them.

```jsx
function LoginForm() {
  const [form, setForm] = useState({ email: '', password: '' });
  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});   // which fields the user has interacted with

  function validate(values) {
    const e = {};
    if (!values.email) e.email = 'Email is required';
    else if (!/\S+@\S+\.\S+/.test(values.email)) e.email = 'Email is invalid';
    if (!values.password) e.password = 'Password is required';
    else if (values.password.length < 8) e.password = 'Min 8 characters';
    return e;
  }

  function handleChange(e) {
    const next = { ...form, [e.target.name]: e.target.value };
    setForm(next);
    setErrors(validate(next));        // live re-validate
  }

  function handleBlur(e) {
    setTouched((t) => ({ ...t, [e.target.name]: true }));
  }

  function handleSubmit(e) {
    e.preventDefault();
    const found = validate(form);
    setErrors(found);
    setTouched({ email: true, password: true });   // reveal all errors on submit
    if (Object.keys(found).length === 0) {
      console.log('submit', form);                 // valid!
    }
  }

  // Show an error only if the field was touched AND has an error.
  const showError = (field) => touched[field] && errors[field];

  return (
    <form onSubmit={handleSubmit} noValidate>
      <div>
        <input name="email" value={form.email} onChange={handleChange} onBlur={handleBlur} />
        {showError('email') && <small style={{ color: 'red' }}>{errors.email}</small>}
      </div>
      <div>
        <input name="password" type="password" value={form.password}
               onChange={handleChange} onBlur={handleBlur} />
        {showError('password') && <small style={{ color: 'red' }}>{errors.password}</small>}
      </div>
      <button type="submit" disabled={Object.keys(errors).length > 0}>Log in</button>
    </form>
  );
}
```

> **UX principle — don't yell too early.** Showing "Email is required" before the user has even touched the field is hostile. Track `touched` and reveal a field's error only after blur or on submit. This single pattern separates amateur forms from polished ones.

> **Gotcha — `noValidate` on the `<form>`.** Add it to disable the browser's native validation bubbles so your React validation is the only UX. Otherwise users see both.

---

## VI. UNCONTROLLED COMPONENTS & REFS

Sometimes you don't need React to track every keystroke — you just want the values on submit. **Uncontrolled** inputs let the DOM hold the value; you read it with a ref. Less code, fewer re-renders.

```jsx
import { useRef } from 'react';

function UncontrolledForm() {
  const formRef = useRef(null);

  function handleSubmit(e) {
    e.preventDefault();
    // Read values straight from the DOM via FormData — no state at all.
    const data = new FormData(e.target);
    console.log(Object.fromEntries(data));   // { username: '...', email: '...' }
  }

  return (
    <form ref={formRef} onSubmit={handleSubmit}>
      {/* defaultValue (not value) sets the INITIAL value for an uncontrolled input */}
      <input name="username" defaultValue="guest" />
      <input name="email" type="email" />
      <button type="submit">Submit</button>
    </form>
  );
}
```

> **Gotcha — `defaultValue`/`defaultChecked`, not `value`/`checked`, for uncontrolled.** Use the `default*` props to set initial values you don't intend to control. Mixing `value` (controlled) and `defaultValue` (uncontrolled) on the same input is a bug.

### File inputs are always uncontrolled

```jsx
function Upload() {
  const fileRef = useRef(null);
  function handleSubmit(e) {
    e.preventDefault();
    const file = fileRef.current.files[0];     // the File object
    if (file) console.log(file.name, file.size);
  }
  return (
    <form onSubmit={handleSubmit}>
      {/* You CANNOT set a file input's value programmatically (security) — it's read-only. */}
      <input type="file" ref={fileRef} accept="image/*" />
      <button type="submit">Upload</button>
    </form>
  );
}
```

> **`<input type="file">` is inherently uncontrolled.** Browsers forbid setting its value from JS (a security measure — a site shouldn't pre-fill files from your disk). Always read it via a ref.

| | Controlled | Uncontrolled |
|---|-----------|--------------|
| Source of truth | React state | DOM |
| Initial value | `value` + state | `defaultValue` |
| Read value | from state, anytime | from ref / FormData, on demand |
| Live validation / formatting | easy | hard |
| Re-render per keystroke | yes | no |
| Best for | most forms | simple forms, file inputs, perf-critical |

---

## VII. REACT HOOK FORM — THE PRODUCTION CHOICE

Hand-rolling controlled state, `touched`, `errors`, and submit handling for large forms gets tedious and re-renders a lot. **React Hook Form (RHF)** embraces uncontrolled inputs under the hood for performance, while giving you validation, error state, and a clean API.

```bash
npm install react-hook-form
```

```jsx
import { useForm } from 'react-hook-form';

function SignupForm() {
  const {
    register,          // connect an input to the form
    handleSubmit,      // wraps your submit, runs validation first
    formState: { errors, isSubmitting },
    reset,             // reset the form
  } = useForm({ defaultValues: { email: '', password: '' } });

  async function onSubmit(data) {
    await new Promise((r) => setTimeout(r, 500));   // pretend API call
    console.log(data);
    reset();                                         // clear on success
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} noValidate>
      <input
        {...register('email', {
          required: 'Email is required',
          pattern: { value: /\S+@\S+\.\S+/, message: 'Invalid email' },
        })}
        placeholder="Email"
      />
      {errors.email && <small>{errors.email.message}</small>}

      <input
        type="password"
        {...register('password', {
          required: 'Password is required',
          minLength: { value: 8, message: 'Min 8 characters' },
        })}
      />
      {errors.password && <small>{errors.password.message}</small>}

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Submitting…' : 'Sign up'}
      </button>
    </form>
  );
}
```

> **Why RHF is fast:** it registers inputs as **uncontrolled** and subscribes to changes surgically, so typing in one field doesn't re-render the whole form. For big forms this is a dramatic difference versus a single controlled state object. The `{...register('name', rules)}` spread wires up `ref`, `onChange`, `onBlur`, and `name` in one shot.

### Controlled components inside RHF (`Controller`)

UI-library inputs (MUI, react-select) are often controlled and don't accept a ref directly. Wrap them with `Controller`:

```jsx
import { useForm, Controller } from 'react-hook-form';
import Select from 'react-select';

function Form() {
  const { control, handleSubmit } = useForm();
  return (
    <form onSubmit={handleSubmit((d) => console.log(d))}>
      <Controller
        name="country"
        control={control}
        rules={{ required: true }}
        render={({ field }) => <Select {...field} options={[/* ... */]} />}
      />
      <button>Go</button>
    </form>
  );
}
```

---

## VIII. ZOD — SCHEMA VALIDATION

Inline validation rules don't scale and can't be reused or shared with the backend. **Zod** defines a typed schema once; it validates *and* (with TypeScript) infers the type. Pair it with RHF via a resolver.

```bash
npm install zod @hookform/resolvers
```

```tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

// Define the shape + rules ONCE. This is the single source of truth.
const schema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Min 8 characters'),
  age: z.coerce.number().min(18, 'Must be 18+'),   // coerce string input → number
  terms: z.literal(true, { errorMap: () => ({ message: 'You must accept' }) }),
});

// TypeScript infers the form's type straight from the schema — no duplicate type.
type FormData = z.infer<typeof schema>;

function RegisterForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),     // Zod now drives all validation
  });

  return (
    <form onSubmit={handleSubmit((d) => console.log(d))} noValidate>
      <input {...register('email')} />
      {errors.email && <small>{errors.email.message}</small>}

      <input type="password" {...register('password')} />
      {errors.password && <small>{errors.password.message}</small>}

      <input type="number" {...register('age')} />
      {errors.age && <small>{errors.age.message}</small>}

      <label><input type="checkbox" {...register('terms')} /> Accept terms</label>
      {errors.terms && <small>{errors.terms.message}</small>}

      <button type="submit">Register</button>
    </form>
  );
}
```

> **Why schema validation wins:** the schema is reusable (validate the same shape on the server), composable (`schema.extend(...)`, `.refine(...)` for cross-field rules like "passwords match"), and with TypeScript gives you the form's type for free via `z.infer`. This is the modern standard for serious forms.

```tsx
// Cross-field validation with .refine — e.g. confirm password.
const pwSchema = z.object({
  password: z.string().min(8),
  confirm: z.string(),
}).refine((data) => data.password === data.confirm, {
  message: "Passwords don't match",
  path: ['confirm'],     // attach the error to the confirm field
});
```

---

## IX. REACT 19 — ACTIONS, `useActionState`, `useOptimistic`, `useFormStatus`

React 19 adds first-class form **Actions**: pass an async function to a `<form>`'s `action`, and React manages pending state, errors, and resets for you. These shine in frameworks (Next.js) but work in client React too.

```jsx
// useActionState — drive a form with an async action and get state + pending back.
import { useActionState } from 'react';

function Subscribe() {
  const [state, formAction, isPending] = useActionState(
    async (prevState, formData) => {
      const email = formData.get('email');
      const res = await subscribe(email);          // your async call
      if (!res.ok) return { error: 'Failed to subscribe' };
      return { success: true };
    },
    { }   // initial state
  );

  return (
    <form action={formAction}>          {/* note: action takes a function, not a URL */}
      <input name="email" type="email" />
      <button disabled={isPending}>{isPending ? 'Subscribing…' : 'Subscribe'}</button>
      {state.error && <p>{state.error}</p>}
      {state.success && <p>Thanks!</p>}
    </form>
  );
}
```

```jsx
// useFormStatus — a child reads the parent form's pending state (no prop drilling).
import { useFormStatus } from 'react-dom';

function SubmitButton() {
  const { pending } = useFormStatus();
  return <button disabled={pending}>{pending ? 'Saving…' : 'Save'}</button>;
}

// useOptimistic — show the expected result instantly, before the server confirms.
import { useOptimistic } from 'react';

function LikeButton({ likes, onLike }) {
  const [optimisticLikes, addOptimistic] = useOptimistic(likes, (cur) => cur + 1);
  return (
    <form action={async () => { addOptimistic(); await onLike(); }}>
      <button>👍 {optimisticLikes}</button>   {/* updates immediately, reconciles after */}
    </form>
  );
}
```

| Hook (React 19) | Purpose |
|------------------|---------|
| `<form action={fn}>` | Run an async function on submit; React tracks pending/errors |
| `useActionState` | Form state + action + pending in one hook |
| `useFormStatus` | Read the enclosing form's pending status from a child |
| `useOptimistic` | Optimistic UI — show the result before the server replies |

> **Gotcha — Actions are newest React.** `useActionState`/`useOptimistic`/`useFormStatus` require React 19+. On React 18 use React Hook Form + manual pending state. Check your React version before relying on these.

---

## X. ACCESSIBLE FORMS

A form that screen readers can't use is broken, no matter how it looks. Accessibility is part of "done."

```jsx
function AccessibleField() {
  const id = useId();                       // stable unique id (file 04)
  const errId = `${id}-error`;
  const [error, setError] = useState('');

  return (
    <div>
      {/* Associate label and input with htmlFor/id so clicking the label focuses the input. */}
      <label htmlFor={id}>Email</label>
      <input
        id={id}
        type="email"
        aria-invalid={!!error}                        // announce invalid state
        aria-describedby={error ? errId : undefined}  // link the error text to the input
      />
      {error && <small id={errId} role="alert">{error}</small>}
    </div>
  );
}
```

Checklist: every input has an associated `<label>`; errors use `role="alert"` and `aria-describedby`; the submit is a real `<button type="submit">`; the form works with keyboard only. More in [`11-Testing-And-TypeScript-React.md`](./11-Testing-And-TypeScript-React.md).

---

## XI. COMMON PITFALLS

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| `value` without `onChange` | Input is read-only, React warns | Add `onChange`, or use `defaultValue`/`readOnly` |
| Initial state `undefined`/`null` | "controlled → uncontrolled" warning | Initialize to `''` / `false` |
| `setForm({ [name]: v })` | Other fields wiped | `setForm(prev => ({ ...prev, [name]: v }))` |
| `<textarea>`/`<select>` like HTML | Value won't bind | Use `value` prop on the element |
| Math on `type="number"` value | String concatenation bugs | `Number(e.target.value)` |
| Forgetting `e.preventDefault()` | Page reloads on submit | Call it in the submit handler |
| Checkbox with `value` not `checked` | Doesn't toggle | Use `checked` + `e.target.checked` |
| Trying to set a file input's value | Doesn't work / error | File inputs are read-only; use a ref |
| Showing errors before interaction | Hostile UX | Track `touched`; reveal on blur/submit |
| Inline rules everywhere | Unmaintainable validation | Zod schema + resolver |
| `useActionState` on React 18 | Undefined / crash | Requires React 19; use RHF instead |

---

## 🧠 KEY TAKEAWAYS

- The defining question is **who owns the value**: **controlled** (React state) or **uncontrolled** (DOM via refs). Controlled is the default for most forms.
- A controlled input needs **both** `value` (bound to state) and `onChange`; initialize state to a **defined** value to avoid the controlled/uncontrolled warning.
- Know the per-input rules: `value` for text/textarea/select, **`checked`** for checkbox/radio, and number inputs return **strings**.
- For many fields, use **one state object + one handler** with a computed key `[name]`, always spreading `prev` to preserve other fields.
- Validate on **submit** and surface field errors only after **touched**/blur; add `noValidate` to own the UX.
- **Uncontrolled** inputs (`defaultValue`, refs, `FormData`) suit simple forms; **file inputs are always uncontrolled**.
- **React Hook Form** scales forms with great performance; **Zod** defines validation once and infers the type — the modern production combo.
- React 19 **Actions** (`useActionState`, `useFormStatus`, `useOptimistic`) make async forms first-class. Always make forms **accessible** (labels, `aria-*`, real submit buttons).

---

**Prev:** [`05-Context-And-State-Management.md`](./05-Context-And-State-Management.md) · **Next:** [`07-Data-Fetching-And-Effects.md`](./07-Data-Fetching-And-Effects.md) · **Index:** [`00-Index.md`](./00-Index.md)
