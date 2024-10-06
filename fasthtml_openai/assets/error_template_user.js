<li x-show="$store.prompts.data[store_data_idx]!=''" class="flex gap-2 items-center w-full text-white p-1 animate-scale-y origin-top">
    <i class="material-icons shrink-0">person</i>
    <p x-text="$store.prompts.data[store_data_idx]"></p>
    <input type="hidden" name="user" x-model="$store.prompts.data[store_data_idx]" />
</li>
