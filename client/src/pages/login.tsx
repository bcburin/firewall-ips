import * as Yup from 'yup';

import {
  Box,
  Button,
  Stack,
  TextField,
  Typography
} from '@mui/material';

import { AuthLayout } from "../layout/auth"
import React from 'react';
import { useFormik } from 'formik';

const LoginPage: React.FC = () => {

  const formik = useFormik({
    initialValues: {
      email: "",
      password: "",
      submit: null,
    },
    validationSchema: Yup.object({
      email: Yup.string()
        .email("Must be a valid email")
        .max(255)
        .required("Email is required"),
      password: Yup.string().max(255).required("Password is required"),
    }),
    onSubmit: async (values, helpers) => {
      // Implement submit logic
      console.log(values);
    },
  });

  return (
    <AuthLayout>
        <Box
        sx={{
          backgroundColor: "background.paper",
          flex: "1 1 auto",
          alignItems: "center",
          display: "flex",
          justifyContent: "center",
        }}
      >
        <Box
          sx={{
            maxWidth: 550,
            px: 3,
            py: "100px",
            width: "100%",
          }}
        >
            <Stack spacing={1} sx={{ mb: 3 }}>
                <Typography variant="h4">Login</Typography>
            </Stack>
            
                <form noValidate onSubmit={formik.handleSubmit} style={{
                    width: "100%"
                }}>
                <Stack spacing={3}>
                        <TextField
                    error={!!(formik.touched.email && formik.errors.email)}
                    fullWidth
                    helperText={formik.touched.email && formik.errors.email}
                    label="Email Address*"
                    name="email"
                    onBlur={formik.handleBlur}
                    onChange={formik.handleChange}
                    type="email"
                    value={formik.values.email}
                    />
                    <TextField
                    error={
                        !!(formik.touched.password && formik.errors.password)
                    }
                    fullWidth
                    helperText={
                        formik.touched.password && formik.errors.password
                    }
                    label="Password*"
                    name="password"
                    onBlur={formik.handleBlur}
                    onChange={formik.handleChange}
                    type="password"
                    value={formik.values.password}
                    />
                </Stack>
                {formik.errors.submit && (
                    <Typography color="error" sx={{ mt: 3 }} variant="body2">
                    {formik.errors.submit}
                    </Typography>
                )}
                <Button
                    fullWidth
                    size="large"
                    sx={{ mt: 3 }}
                    type="submit"
                    variant="contained"
                >
                    Continue
                </Button>
                </form>
            
        </Box>
        </Box>
    </AuthLayout>
  );
};

export default LoginPage;