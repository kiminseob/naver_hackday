/* 
**  mod_mod_inseop.c -- Apache sample mod_inseop module
**  [Autogenerated via ``apxs -n mod_inseop -g'']
**
**  To play with this sample module first compile it into a
**  DSO file and install it into Apache's modules directory 
**  by running:
**
**    $ apxs -c -i mod_mod_inseop.c
**
**  Then activate it in Apache's apache2.conf file for instance
**  for the URL /mod_inseop in as follows:
**
**    #   apache2.conf
**    LoadModule mod_inseop_module modules/mod_mod_inseop.so
**    <Location /mod_inseop>
**    SetHandler mod_inseop
**    </Location>
**
**  Then after restarting Apache via
**
**    $ apachectl restart
**
**  you immediately can request the URL /mod_inseop and watch for the
**  output of this module. This can be achieved for instance via:
**
**    $ lynx -mime_header http://localhost/mod_inseop 
**
**  The output should be similar to the following one:
**
**    HTTP/1.1 200 OK
**    Date: Tue, 31 Mar 1998 14:42:22 GMT
**    Server: Apache/1.3.4 (Unix)
**    Connection: close
**    Content-Type: text/html
**  
**    The sample page from mod_mod_inseop.c
*/ 

#include "httpd.h"
#include "http_config.h"
#include "http_protocol.h"
#include "ap_config.h"
#include <curl/curl.h>

struct string {
  char *ptr;
  size_t len;
};

void init_string(struct string *s) {
  s->len = 0;
  s->ptr = malloc(s->len+1);
  if (s->ptr == NULL) {
    fprintf(stderr, "malloc() failed\n");
    exit(EXIT_FAILURE);
  }
  s->ptr[0] = '\0';
}

size_t writefunc(void *ptr, size_t size, size_t nmemb, struct string *s)
{
  size_t new_len = s->len + size*nmemb;
  s->ptr = realloc(s->ptr, new_len+1);
  if (s->ptr == NULL) {
    fprintf(stderr, "realloc() failed\n");
    exit(EXIT_FAILURE);
  }
  memcpy(s->ptr+s->len, ptr, size*nmemb);
  s->ptr[new_len] = '\0';
  s->len = new_len;

  return size*nmemb;
}


/* The sample content handler */
static int mod_inseop_handler(request_rec *r)
{
    if (strcmp(r->handler, "mod_inseop")) {
        return DECLINED;
    }
    r->content_type = "text/html";      

    if (!r->header_only)
        ap_rprintf(r, "%s\n", r->unparsed_uri);
    //char token[100];
    //*token = strtok(r->unparsed_uri,"?search=");
    //ap_rprintf(r, "%s\n", token);

	
    CURL *curl;
    CURLcode res;

    curl_global_init(CURL_GLOBAL_ALL);

    curl = curl_easy_init();
    if(curl) {
	    struct string s;
            init_string(&s);
			
            curl_easy_setopt(curl, CURLOPT_URL, "localhost:2001/naver_crawler_search/index.html");
            curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, writefunc);
    	    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &s);
	    res = curl_easy_perform(curl);

            if(res != CURLE_OK)
                    fprintf(stderr, "curl_easy_perform() failed: %s\n",
                                    curl_easy_strerror(res));
	    printf("%s\n",s.ptr);	
            free(s.ptr);
	    curl_easy_cleanup(curl);
    }
   


    return OK;
}

static void mod_inseop_register_hooks(apr_pool_t *p)
{
    ap_hook_handler(mod_inseop_handler, NULL, NULL, APR_HOOK_MIDDLE);
}



/* Dispatch list for API hooks */
module AP_MODULE_DECLARE_DATA mod_inseop_module = {
    STANDARD20_MODULE_STUFF, 
    NULL,                  /* create per-dir    config structures */
    NULL,                  /* merge  per-dir    config structures */
    NULL,                  /* create per-server config structures */
    NULL,                  /* merge  per-server config structures */
    NULL,                  /* table of config file commands       */
    mod_inseop_register_hooks  /* register hooks                      */
};

