export default () => {
  const { mdAndUp } = useDisplay()

  const width = computed(() => {
    if (!mdAndUp) {
      return '100%'
    }
    return '600px'
  })

  const height = computed(() => {
    if (!mdAndUp) {
      return '100%'
    }
    return '700px'
  })

  return {
    width,
    height
  }
}
