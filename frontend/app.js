(() => {
  const { useEffect, useMemo, useState, useCallback, useRef } = React;

  const STORAGE_KEY = 'auth_token';
  const BASE_URL = window.BACKEND_BASE_URL || '';

  async function http(path, options) {
    const res = await fetch(BASE_URL + path, {
      headers: { 'Content-Type': 'application/json', ...(options && options.headers), method: (options && options.method)},
      ...(options || {}),
    });
    const isJson = (res.headers.get('content-type') || '').includes('application/json');
    const data = isJson ? await res.json() : null;
    if (!res.ok) {
      const message = (data && (data.message || data.error)) || res.statusText;
      throw new Error(message);
    }
    return data;
  }

  function useAuth() {
    const [token, setToken] = useState(() => localStorage.getItem(STORAGE_KEY));
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const saveToken = useCallback((t) => {
      setToken(t);
      if (t) localStorage.setItem(STORAGE_KEY, t); else localStorage.removeItem(STORAGE_KEY);
    }, []);

    const verify = useCallback(async () => {
      if (!token) return false;
      try {
        const res = await http('/verify_token', { method: 'POST', body: JSON.stringify({ token }) });
        return !!(res && res.valid);
      } catch (e) {
        saveToken('');
        return false;
      }
    }, [token, saveToken]);

    const login = useCallback(async (username, password) => {
      setLoading(true); setError('');
      try {
        const res = await http('/get_token/' + username +"/" +password, { method: 'GET'});
        saveToken(res.token);
        return true;
      } catch (e) {
        setError(e.message);
        return false;
      } finally { setLoading(false); }
    }, [saveToken]);

    const register = useCallback(async (payload) => {
      setLoading(true); setError('');
      try {
        const res = await http('/register', { method: 'POST', body: JSON.stringify(payload) });
        return res.user_id;
      } catch (e) {
        setError(e.message); return null;
      } finally { setLoading(false); }
    }, []);

    const createSystemUser = useCallback(async (userId, system_user_name, password, role = 'admin') => {
      setLoading(true); setError('');
      try {
        await http(`/create_system_user/${userId}`, {
          method: 'POST',
          body: JSON.stringify({ system_user_name, password, role })
        });
        return true;
      } catch (e) { setError(e.message); return false; } finally { setLoading(false); }
    }, []);

    return { token, loading, error, saveToken, verify, login, register, createSystemUser };
  }

  function PropertyCard({ item, isAuthenticated, onAuthRequired }) {
    return React.createElement('div', {
      className: 'card',
      onClick: isAuthenticated ? undefined : onAuthRequired
    },
      React.createElement('img', {
        className: 'thumb',
        src: item.imageUrl,
        alt: item.address,
        onError: (e) => { e.currentTarget.src = 'https://picsum.photos/400/300?blur=1'; }
      }),
      React.createElement('div', { className: 'content' },
        React.createElement('div', { className: 'addr' }, item.address),
        React.createElement('div', { className: 'desc' },
          isAuthenticated ? item.description : 'התחבר כדי לראות פרטים נוספים'
        ),
        React.createElement('div', { className: 'price' },
          isAuthenticated && item.price ? `${item.price.toLocaleString()} ₪` : ''
        )
      )
    );
  }

  function AuthModal({ step, setStep, onClose, onSuccess, auth }) {
    const [form, setForm] = useState({ id: '', first_name: '', last_name: '', email: '', phone_number: '' });
    const [creds, setCreds] = useState({ username: '', password: '' });
    const [userId, setUserId] = useState(null);

    const canContinueReg = form.id && form.first_name && form.last_name && form.email && form.phone_number;
    const canContinueCreds = creds.username && creds.password;

    const onSubmitReg = async () => {
      const uid = await auth.register({ ...form, reputation_score: 0 });
      if (uid) { setUserId(uid); setStep('creds'); }
    };

    const onSubmitCreds = async () => {
      const created = await auth.createSystemUser(userId, creds.username, creds.password, 'admin');
      if (created) {
        const ok = await auth.login(creds.username, creds.password);
        if (ok) { onSuccess(); }
      }
    };

    const onSubmitLogin = async () => {
      const ok = await auth.login(creds.username, creds.password);
      if (ok) { onSuccess(); }
    };

    return React.createElement('div', { className: 'modal', onClick: onClose },
      React.createElement('div', { className: 'sheet', onClick: (e) => e.stopPropagation() },
        React.createElement('header', null, step === 'register' ? 'הרשמה' : step === 'creds' ? 'יצירת שם משתמש' : 'התחברות'),
        React.createElement('div', { className: 'body' },
          auth.error && React.createElement('div', { className: 'error' }, auth.error),
          step === 'register' && [
            ['id','תעודת זהות'],['first_name','שם פרטי'],['last_name','שם משפחה'],['email','אימייל'],['phone_number','טלפון']
          ].map(([key,label]) => React.createElement('input', {
            key, className: 'input', placeholder: label, value: form[key] || '', onChange: e => setForm(f => ({ ...f, [key]: e.target.value }))
          })),
          step !== 'register' && [
            React.createElement('input', { key: 'u', className: 'input', placeholder: 'שם משתמש', value: creds.username, onChange: e => setCreds(c => ({ ...c, username: e.target.value })) }),
            React.createElement('input', { key: 'p', type: 'password', className: 'input', placeholder: 'סיסמה', value: creds.password, onChange: e => setCreds(c => ({ ...c, password: e.target.value })) })
          ]
        ),
        React.createElement('footer', null,
          React.createElement('button', { className: 'btn', onClick: onClose }, 'סגור'),
          step === 'register' && React.createElement('button', { className: 'btn primary', disabled: auth.loading || !canContinueReg, onClick: onSubmitReg }, auth.loading ? 'שולח...' : 'המשך'),
          step === 'creds' && React.createElement('button', { className: 'btn primary', disabled: auth.loading || !canContinueCreds, onClick: onSubmitCreds }, auth.loading ? 'יוצר...' : 'צור והתחבר'),
          step === 'login' && React.createElement('button', { className: 'btn primary', disabled: auth.loading || !canContinueCreds, onClick: onSubmitLogin }, auth.loading ? 'מתחבר...' : 'התחבר')
        )
      )
    );
  }

  function App() {
    const auth = useAuth();
    const [showModal, setShowModal] = useState(false);
    const [modalStep, setModalStep] = useState('register');

    const properties = useMemo(() => {
      const sample = [];
      for (let i = 1; i <= 20; i++) {
        sample.push({
          id: i,
          imageUrl: `https://picsum.photos/seed/p${i}/400/300` ,
          address: `רחוב הפרדס ${i}, תל אביב`,
          description: 'דירה מוארת ומרווחת עם נוף פתוח ונגישות גבוהה',
          price: 1500000 + i * 10000
        });
      }
      return sample;
    }, []);

    useEffect(() => { (async () => { await auth.verify(); })(); }, []);

    const onAuthRequired = () => {
      setModalStep('register');
      setShowModal(true);
    };

    const onSuccessAuth = () => {
      setShowModal(false);
    };

    return React.createElement('div', { className: 'container' },
      React.createElement('div', { className: 'header' },
        React.createElement('div', { className: 'title' }, 'נכסים זמינים'),
        React.createElement('div', null,
          auth.token ? React.createElement('button', { className: 'btn', onClick: () => auth.saveToken('') }, 'התנתק') :
          React.createElement('button', { className: 'btn primary', onClick: () => { setModalStep('login'); setShowModal(true); } }, 'התחבר'),
          React.createElement('button', { className: 'btn primary', onClick: () => { setModalStep('add_asset'); setShowModal(true); } }, 'הוספת נכס למכירה')
        )
      ),
      React.createElement('div', { className: 'grid' },
        properties.map(p => React.createElement(PropertyCard, {
          key: p.id,
          item: p,
          isAuthenticated: !!auth.token,
          onAuthRequired: onAuthRequired
        }))
      ),
      showModal && React.createElement(AuthModal, {
        step: modalStep,
        setStep: setModalStep,
        onClose: () => setShowModal(false),
        onSuccess: onSuccessAuth,
        auth
      })
    );
  }

  ReactDOM.createRoot(document.getElementById('root')).render(React.createElement(App));
})();