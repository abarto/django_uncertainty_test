# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"

  config.vm.define "django-uncertainty-test-vm" do |vm_define|
  end

  config.vm.hostname = "django-uncertainty-test.local"

  config.vm.network "forwarded_port", guest: 80, host: 8000
  config.vm.network "forwarded_port", guest: 8000, host: 8001

  config.vm.synced_folder ".", "/home/vagrant/django_uncertainty_test/"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
    vb.cpus = 1
    vb.name = "django-uncertainty-test"
  end

  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y supervisor nginx git build-essential python3 python3.4-venv
  SHELL

  config.vm.provision "shell", privileged: false, inline: <<-SHELL
    pyvenv-3.4 --without-pip django_uncertainty_test_venv
    source django_uncertainty_test_venv/bin/activate
    curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | python

    pip install -r django_uncertainty_test/requirements.txt

    cd django_uncertainty_test/django_uncertainty_test/

    python manage.py migrate
    python manage.py loaddata data.json
    python manage.py collectstatic --noinput
  SHELL

  config.vm.provision "shell", inline: <<-SHELL
    echo '
upstream django_uncertainty_test_upstream {
    server 127.0.0.1:8000 fail_timeout=0;
}

server {
    listen 80;
    server_name localhost;

    client_max_body_size 4G;

    access_log /home/vagrant/django_uncertainty_test/nginx_access.log;
    error_log /home/vagrant/django_uncertainty_test/nginx_error.log;

    location /static/ {
        alias /home/vagrant/django_uncertainty_test/django_uncertainty_test/static/;
    }

    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        if (!-f $request_filename) {
            proxy_pass http://django_uncertainty_test_upstream;
            break;
        }
    }
}
    ' > /etc/nginx/conf.d/django_uncertainty_test.conf

    /usr/sbin/service nginx restart
  SHELL

  config.vm.provision "shell", run: "always", privileged: false, inline: <<-SHELL
    source /home/vagrant/django_uncertainty_test_venv/bin/activate
    cd /home/vagrant/django_uncertainty_test/django_uncertainty_test
    gunicorn --bind 127.0.0.1:8000 --daemon --workers 1 django_uncertainty_test.wsgi
  SHELL
end
