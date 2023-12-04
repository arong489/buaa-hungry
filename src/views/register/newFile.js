import { reactive } from 'vue';
import { useRouter } from 'vue-router';
import { ref } from 'vue';

export default (await
    import ('vue')).defineComponent({
    components: { MyHeader },
    setup() {
        const router = useRouter();
        const data = reactive({
            username: '',
            pwd: ''
        });
        const avatar = ref({});
    }
});