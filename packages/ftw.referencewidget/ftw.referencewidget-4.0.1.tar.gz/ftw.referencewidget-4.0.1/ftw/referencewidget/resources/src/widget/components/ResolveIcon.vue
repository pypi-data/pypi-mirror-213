<template>
  <div class="d-inline-block me-1">
    <template v-if="item['@type'] == 'File'">
      <img
        :src="`${item['@id']}/@@iconresolver/mimetype-${item['mime_type']}`"
      />
    </template>
    <template v-else-if="item['@type'] == 'Image'">
      <img
        :src="`${item['@id']}/@@iconresolver/mimetype-${item['mime_type']}`"
      />
    </template>
    <template v-else>
      <img
        :src="`${item['@id']}/@@iconresolver/${iconMapping[item['@type']]}`"
      />
    </template>
  </div>
</template>
<script>
export default {
  props: {
    item: {
      type: Object,
      required: true,
      default: () => {
        return {};
      },
    },
    iconMapping: {
      type: Object,
      required: true,
      default: () => {
        return {};
      },
    },
  },
};
</script>
