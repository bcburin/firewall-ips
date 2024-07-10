import { PaletteOptions, SimplePaletteColorOptions, TypeAction, alpha } from "@mui/material/styles";
import { darkIndigo, error, info, neutral, success, warning } from "./colors";

import { common } from "@mui/material/colors";

export interface LocalPaletteOptions extends PaletteOptions {
  primary: SimplePaletteColorOptions;
  error: SimplePaletteColorOptions;
  action: Partial<TypeAction>;
  neutral: {
    50: string;
    100: string;
    200: string;
    300: string;
    400: string;
    500: string;
    600: string;
    700: string;
    800: string;
    900: string;
  };
}

export function createPalette(): LocalPaletteOptions {
  return {
    action: {
      active: neutral[500],
      disabled: alpha(neutral[900], 0.38),
      disabledBackground: alpha(neutral[900], 0.12),
      focus: alpha(neutral[900], 0.16),
      hover: alpha(neutral[900], 0.04),
      selected: alpha(neutral[900], 0.12),
    },
    background: {
      default: common.white,
      paper: common.white,
    },
    divider: "#F2F4F7",
    error,
    neutral,
    info,
    mode: "light",
    primary: darkIndigo,
    success,
    text: {
      primary: neutral[900],
      secondary: neutral[500],
      disabled: alpha(neutral[900], 0.38),
    },
    warning,
  };
}
