#!/bin/sh -e

cd ${envroot}

export RATTAIL_CONFIG_FILES=${overnight_conf}

bin/rattail overnight -k ${automation.lower()} <%text>\</%text>
        --no-versioning <%text>\</%text>
        % if email_key is not Undefined and email_key:
        --email-key '${email_key}' <%text>\</%text>
        % endif
        --no-email-if-empty <%text>\</%text>
        --wait
