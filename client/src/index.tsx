import { CssBaseline, ThemeProvider } from '@mui/material';

import App from './App';
import ReactDOM from 'react-dom/client';
import { createTheme } from './theme/index'

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);
root.render(
      <ThemeProvider theme={ createTheme() }>
        <CssBaseline />
        <App />
      </ThemeProvider>
);
