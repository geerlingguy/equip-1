import { ref } from 'vue'

const modelColor = ref('#5500ff')

export function useModelColor() {
  const setColor = (color: string) => {
    modelColor.value = color
  }

  return {
    modelColor,
    setColor
  }
}
