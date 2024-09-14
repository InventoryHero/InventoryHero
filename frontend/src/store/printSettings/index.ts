import {defineStore} from "pinia";

export type StorageIconSizes = 'x-small'|'small'|'default'|'large'|'x-large'
export type Paper = 'A4'|'A5'
type QrCodeScales = {
    [key: string]: number
}


export const supportedPapers = ['A4', 'A5']


export type Margins = {
    left?: number,
    right?: number,
    top?: number,
    bottom?: number
}


interface PrintSettings {
    qrCodeIconWidth?: number,
    fontSize?: number,
    rows?: number,
    cols?: number,
    paper?: 'A4'|'A5',
    storageIconSize?: StorageIconSizes,
    qrCodeIconVisible?: boolean,
    qrCodeVisible?: boolean,
    storageIconVisible?: boolean
    storageNameVisible?: boolean,
    storageLabelVisible?: boolean,
    borderThickness?: number,
    storageIcon?: string,
    margins?: Margins
}

// TODO FIND A BETTER WAY TO GET SCALES
const paperSizes = {
    A4: {
        name: "A4",
        width: 210,
        height: 297,
        scales: {
            "9": 110, "10": 100, "11": 90, "12": 80, "13": 75, "14": 70, "15": 65, "default": 120
        } as QrCodeScales
    },
    A5: {
        name: "A5",
        width: 148,
        height: 210,
        scales: {
            "9": 75, "10": 65, "11": 60, "12": 55, "13": 50, "14": 45, "15": 45, "default": 85
        } as QrCodeScales
    },
    // Add more sizes as needed
};


export default defineStore("printSettings", {
    state: () => {
        return {
            settings: {} as PrintSettings,
            _previewScale: 68
        }
    },
    actions: {
        setStorageLabel(value: boolean){
            this.settings.storageLabelVisible = value
        },
        setStorageNameVisible(value: boolean){
            this.settings.storageNameVisible = value
        },
        setStorageIconVisible(value: boolean){
            this.settings.storageIconVisible = value
        },
        setBorderThickness(value: number){
            this.settings.borderThickness = Math.max(Math.min(8, value), 0)
        },
        setQrCodeVisible(value: boolean){
            this.settings.qrCodeVisible = value
        },
        setQrCodeIconVisible(value: boolean){
            this.settings.qrCodeIconVisible = value
        },
        setQrCodeIconWidth(value: number){
            this.settings.qrCodeIconWidth = Math.max(0, Math.min(value, 50))
        },
        setStorageIconSize(value: StorageIconSizes){
            this.settings.storageIconSize = value
        },
        setFontSize(value: number){
            this.settings.fontSize = value
        },
        setColumns(value: number){
            this.settings.cols = Math.max(Math.min(5, value), 1)
        },
        setRows(value: number){
            this.settings.rows = Math.max(Math.min(15, value), 1)
        },
        setPaper(value: Paper){
            this.settings.paper = value
        },
        setMargin(margin: 'left'|'right'|'top'|'bottom', value: number){
            this.settings.margins = {
                ...this.settings.margins,
            }
            this.settings.margins[margin] = Math.min(Math.max(0, value), 30)
        },
        setPreviewScale(value: number){
            this._previewScale = Math.max(0, Math.min(100, value))
        },
        reset(){
            this.settings = {}
            this._previewScale = 68
        }
    },
    getters: {
        storageLabelVisible: state => state.settings.storageLabelVisible ?? true,
        storageNameVisible: state => state.settings.storageNameVisible ?? true,
        storageIconVisible: state => state.settings.storageIconVisible ?? true,
        borderThickness: state => state.settings.borderThickness ?? 2,
        qrCodeVisible: state => state.settings.qrCodeVisible ?? true,
        qrCodeIconVisible: state => state.settings.qrCodeIconVisible ?? true,
        qrCodeIconWidth: state => state.settings.qrCodeIconWidth ?? 50,
        storageIconSize: state => state.settings.storageIconSize ?? 'default',
        fontSize: state => state.settings.fontSize ?? 12,
        columns: state => state.settings.cols ?? 3,
        rows: state => state.settings.rows ?? 8,
        paper: state => paperSizes[state.settings.paper ?? 'A4'],
        qrCodeScale: state => Math.floor((297 / (state.settings.rows ?? 8)) / 7),
        margins: state => {
            return {
                left: 10,
                right: 10,
                bottom: 10,
                top: 10,
                ...state.settings.margins
            }
        },
        previewScale: state => state._previewScale
    }
})
