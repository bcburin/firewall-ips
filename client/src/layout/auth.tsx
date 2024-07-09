import { Box, Unstable_Grid2 as Grid } from "@mui/material";

import PropTypes from "prop-types";

export const AuthLayout = ({ children }: any) => {

  return (
    <Box
      component="main"
      sx={{
        display: "flex",
        flex: "1 1 auto",
        minHeight: "100vh"  // TODO: find better solution
      }}
    >
      <Grid container sx={{
        flex: "1 1 auto" 
        }}>
        <Grid
          xs={12}
          lg={6}
          sx={{
            backgroundColor: "background.paper",
            display: "flex",
            flexDirection: "column",
            position: "relative",
            width: "100%"
          }}
        >
          {children}
        </Grid>
        <Grid
          xs={12}
          lg={6}
          sx={{
            alignItems: "center",
            background:
              "radial-gradient(50% 50% at 50% 50%, #122647 0%, #090E23 100%)",
            color: "white",
            display: "flex",
            justifyContent: "center",
            "& img": {
              maxWidth: "100%",
            },
          }}
        ></Grid>
      </Grid>
    </Box>
  );
};

AuthLayout.prototypes = {
  children: PropTypes.node,
};
