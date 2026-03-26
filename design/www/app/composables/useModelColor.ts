import { ref } from 'vue'

type ModelType = 'equip-1' | 'firehat'

const currentModel = ref<ModelType>('equip-1')

export function useModelColor() {
  return {
    currentModel,
    setModel: (model: ModelType) => currentModel.value = model
  }
}
