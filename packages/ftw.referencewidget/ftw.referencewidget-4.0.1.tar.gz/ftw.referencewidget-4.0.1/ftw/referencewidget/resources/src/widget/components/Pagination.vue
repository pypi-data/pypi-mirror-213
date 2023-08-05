<template>
  <nav aria-label="Pagination for this listing" v-if="batching['@id']">
    <ul class="pagination">
      <li :class="batching.prev ? 'page-item' : 'page-item disabled'">
        <a href="#" @click.prevent="triggerPrevious" class="page-link">
          {{ $i18n("Previous") }}
        </a>
      </li>
      <li>
        <span class="page-link">
          {{ $i18n("Page") }} {{ page }} {{ $i18n("of") }} {{ Math.trunc(items_total / b_size) + 1 }}
        </span>
      </li>
      <li :class="batching.next ? 'page-item' : 'page-item disabled'">
        <a href="#" @click.prevent="triggerNext" class="page-link">
          {{ $i18n("Next") }}
        </a>
      </li>
    </ul>
  </nav>
</template>
<script>
import qs from "qs";

export default {
  props: {
    batching: {
      type: Object,
      required: true,
      default: () => {
        return null;
      },
    },
    items_total: {
      type: Number,
      required: true,
      default: () => {
        return 0;
      },
    },
  },
  data() {
    return {
      b_size: 25,
      b_start: 0,
      page: 1,
    };
  },
  watch: {
    batching: {
      handler(newValue) {
        const query = qs.parse(newValue["@id"].split("?")[1]);
        this.b_size = query.b_size ? parseInt(query.b_size) : 25;
        this.b_start = query.b_start ? parseInt(query.b_start) : 0;
        this.page = this.b_start != 0 ? this.b_start / this.b_size + 1 : 1;
      },
      deep: true,
    },
  },
  methods: {
    get_url_query(url) {
      const [path, querystring] = url.split("?");
      return [path, qs.parse(querystring)];
    },
    triggerNext() {
      const [url, query] = this.get_url_query(this.batching.next);
      this.$emit("next", url, query);
    },
    triggerPrevious() {
      const [url, query] = this.get_url_query(this.batching.prev);
      this.$emit("previous", url, query);
    },
  },
};
</script>
