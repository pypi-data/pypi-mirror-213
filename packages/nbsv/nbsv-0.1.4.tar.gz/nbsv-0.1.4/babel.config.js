module.exports = {
  sourceMap: 'inline',
  presets: [
    [
      '@babel/preset-env',
      {
        "modules": "auto",
        targets: {
          node: 'current',
        },
      },
    ],
    ["@babel/preset-typescript"],
    ["@babel/preset-react"]
  ],
  plugins: ['@babel/transform-runtime', 'babel-plugin-transform-import-meta'],
};
