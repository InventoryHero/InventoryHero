import { defineStore } from 'pinia'

export type StorageIconSizes =
  | 'x-small'
  | 'small'
  | 'default'
  | 'large'
  | 'x-large'
export type Paper = 'A4' | 'A5'
type QrCodeScales = {
  [key: string]: number
}
export type Margins = {
  left: number
  right: number
  top: number
  bottom: number
}

// TODO FIND A BETTER WAY TO GET SCALES
export const paperSizes = {
  A4: {
    name: 'A4',
    width: 210,
    height: 297,
    scales: {
      '9': 110,
      '10': 100,
      '11': 90,
      '12': 80,
      '13': 75,
      '14': 70,
      '15': 65,
      default: 120
    } as QrCodeScales
  },
  A5: {
    name: 'A5',
    width: 148,
    height: 210,
    scales: {
      '9': 75,
      '10': 65,
      '11': 60,
      '12': 55,
      '13': 50,
      '14': 45,
      '15': 45,
      default: 85
    } as QrCodeScales
  }
  // Add more sizes as needed
}
type PaperSizes = keyof typeof paperSizes

export default defineStore('printSettings', () => {
  const storageLabelVisible = ref<boolean>(false)
  const storageNameVisible = ref<boolean>(true)
  const storageIconVisible = ref<boolean>(true)
  const borderThickness = ref<number>(2)
  const qrCodeVisible = ref<boolean>(true)
  const qrCodeIconVisible = ref<boolean>(true)
  const qrCodeIconWidth = ref<number>(35)
  const storageIconSize = ref<number>(24)
  const fontSize = ref<number>(12)
  const columns = ref<number>(3)
  const rows = ref<number>(8)
  const paper = ref<PaperSizes>('A4')
  const qrCodeScale = ref<number>(
    Math.floor(paperSizes[paper.value].height / rows.value / 7)
  )
  const margins = ref<Margins>({
    left: 10,
    right: 10,
    bottom: 10,
    top: 10
  })

  return {
    storageLabelVisible,
    storageNameVisible,
    storageIconVisible,
    borderThickness,
    qrCodeVisible,
    qrCodeIconVisible,
    qrCodeIconWidth,
    fontSize,
    columns,
    rows,
    paper,
    storageIconSize,
    qrCodeScale,
    margins
  }
})
