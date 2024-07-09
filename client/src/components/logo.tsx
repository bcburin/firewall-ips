import DirectionsCarFilledRoundedIcon from "@mui/icons-material/DirectionsCarFilledRounded";
import { useTheme } from "@mui/material/styles";

export const Logo = () => {
  const theme = useTheme();
  const fillColor = theme.palette.primary.main;

  return (
    <DirectionsCarFilledRoundedIcon
      style={{ fill: fillColor }}
      fontSize="large"
    />
  );
};
