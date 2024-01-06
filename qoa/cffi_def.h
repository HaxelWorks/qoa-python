
#define QOA_MAX_CHANNELS 8
#define QOA_LMS_LEN 4
typedef struct {
	int history[QOA_LMS_LEN];
	int weights[QOA_LMS_LEN];
} qoa_lms_t;

typedef struct {
	unsigned int channels;
	unsigned int samplerate;
	unsigned int samples;
	qoa_lms_t lms[QOA_MAX_CHANNELS];
} qoa_desc;

void *qoa_read(const char *filename, qoa_desc *qoa);
int qoa_write(const char *filename, const short *sample_data, qoa_desc *qoa);
void *qoa_encode(const short *sample_data, qoa_desc *qoa, unsigned int *out_len);
// short *qoa_decode(const unsigned char *bytes, int size, qoa_desc *file);

void free(void *ptr);
