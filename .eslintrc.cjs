module.exports = {
  root: true,
  parserOptions: {
    project: './tsconfig.json'
  },
  extends: ['next/core-web-vitals', 'eslint:recommended', 'plugin:prettier/recommended'],
  rules: {
    'prettier/prettier': ['error']
  }
}
