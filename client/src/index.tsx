import { CssBaseline, ThemeProvider } from '@mui/material';

import App from './App';
import { Provider } from 'react-redux';
import ReactDOM from 'react-dom/client';
import { createTheme } from './theme/index'
import { store } from './store/store';

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);
root.render(
  <Provider store={store}>
    <ThemeProvider theme={createTheme()}>
      <CssBaseline />
      <App />
    </ThemeProvider>
  </Provider>
);
