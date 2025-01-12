// src/environments/environment.ts
export const environmentProd = {
    production: true,
    apiUrl: '/api/v1',
    ignoreCertificateErrors: true,
};

export const environmentDev = {
    production: false,
    apiUrl: '/api/v1',
    ignoreCertificateErrors: true,
};

// disable for now
// function getEnv(variableName: string): string {
//     const value = process.env[variableName];
//     if (value === undefined || value === null) {
//         throw new Error(`Environment variable ${variableName} is not set.`);
//     }
//     return value;
// }
