<script setup lang="ts">
import { type APIResponse } from '~/typings';
definePageMeta({
  layout: 'dash'
})
const { data } = await useFetch<APIResponse>('/api/products')

const items = data.value?.body

const cart = reactive(process.client ? JSON.parse(localStorage.getItem('cart') || '[]') : [])

function addToCart(id: number) {
  if (!process.client) return
  cart.push(items.value.find((item: any) => item.id === id))
  localStorage.setItem('cart', JSON.stringify(cart))
}

const cartHas = computed(() => (item: any) => cart.some((i: any) => i.id === item.id))
</script>
<template>
  <Title>Store</Title>
  <div class="container flex flex-col mx-auto p-4">

    <div class="flex justify-end mb-4">
      <NuxtLink to="/cart" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">View Cart
      </NuxtLink>
    </div>

    <hr class="mb-4">

    <div class="flex flex-wrap gap-4">
      <div v-for="item in items" :key="item.id" class="bg-white p-4 rounded-lg border border-gray-200 w-[350px] px-4"
        style="max-width: 330px;">
        <img :src="item.image" alt="" class="w-full h-40 object-cover rounded-lg">
        <div class="mt-4">
          <h3 class="text-lg font-semibold" style="text-transform: capitalize;">{{ item.name }}</h3>
          <p class="text-sm text-gray-500">{{ item.description }}</p>
          <div class="flex justify-between items-center mt-4">
            <p class="text-lg font-bold">{{ item.price }}</p>
            <ClientOnly>
              <button class="px-4 py-2 bg-emerald-500 text-white rounded hover:bg-emerald-600" v-if="item.stock > 0"
                @click="addToCart(item.id)" :disabled="cartHas(item)">Add to
                Cart
              </button>
            </ClientOnly>
            <p class="text-red-500" v-if="item.stock <= 0">Out of Stock</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>
button:disabled {
  cursor: not-allowed;
  background-color: #ccc;
}
</style>