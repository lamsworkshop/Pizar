# Pizar
Scratch 3.0 Extension for Pizar (raspberry PI Zero cAR)

## Copy Files to Scratch Sources
index.js: copy it to scratch-vm/src/extensions/scratch3_pizar/

pizar.png: copy it to scratch-gui/src/lib/libraries/extensions/pizar/

pizar-small.svg: copy it to scratch-gui/src/lib/libraries/extensions/pizar/

## Modify Scratch Code
### scratch-vm/src/extension-support/extension-manager.js
add item to **builtinExtensions**:
```
pizar: () => require('../extensions/scratch3_pizar')
```
### scratch-gui/src/lib/library/extensions/index.jsx
add import:
```
import pizarIconURL from './pizar/pizar.png';
import pizarInsetIconURL from './pizar/pizar-small.svg';
```
add item to **default**:
```
    {
        name: (
            <FormattedMessage
                defaultMessage="Pizar"
                description="Name for the 'Pizar' extension"
                id="gui.extension.pizar.name"
            />
        ),
        // This must be your extension's ID.
        extensionId: 'pizar',
        collaborator: 'Lams Workshop',
        // This is the big image in the extension library.
        iconURL: pizarIconURL,
        // This is the small image in the extension library.
        insetIconURL: pizarInsetIconURL,
        description: (
            <FormattedMessage
                defaultMessage="Raspberry Pi Zero Car"
                description="Description for the 'Dialogs' extension"
                id="gui.extension.pizar.description"
            />
        ),
        // Currently, all extensions in Scratch are featured. Setting this to false simply makes the extension appear smaller in the library.
        featured: true,
        disabled: false,
        internetConnectionRequired: true
    }
```
## Build Prerequisite
node.js and react.js

## Procedures
```
$git clone https://github.com/scratchfoundation/scratch-gui.git --depth=1
$git clone https://github.com/scratchfoundation/scratch-vm.git --depth=1
**Modify Code**
$cd scratch-vm/
$npm install
$npm link
$cd ../scratch-gui/
$npm install
$npm link ../scratch-vm/
$npm start
```

