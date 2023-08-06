module.exports = {
  automock: false,
  testEnvironment: "jsdom",
  moduleNameMapper: {
    '\\.(css|less|sass|scss)$': 'identity-obj-proxy',
  },
  preset: 'ts-jest/presets/js-with-babel',
  transform: {
    '^.+\\.tsx$': 'babel-jest',
  },
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],
  transformIgnorePatterns: [
    "node_modules/(?!@ngrx|(?!deck.gl)|ng-dynamic)"
  ],
  testRegex: '/__tests__/.*.spec.ts[x]?$',
  globals: {
    TextEncoder: require('util').TextEncoder,
  }
};
