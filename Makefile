PROJECT_NAME ?= enrollment2022
VERSION = $(shell python3 setup.py --version | tr '+' '-')
PROJECT_NAMESPACE ?= iriskis
REGISTRY_IMAGE ?= $(PROJECT_NAMESPACE)/$(PROJECT_NAME)

all:
	@echo "make devenv		- Create & setup development virtual environment"
	@echo "make postgres	- Start postgres container"
	@echo "make clean		- Remove files created by distutils"
	@echo "make test		- Run tests"
	@echo "make sdist		- Make source distribution"
	@echo "make docker		- Build a docker image"
	@echo "make upload		- Upload docker image to the registry"
	@exit 0

clean:
	rm -fr *.egg-info dist

devenv: clean
	rm -rf env
	# создаем новое окружение
	python3.8 -m venv env
	# обновляем pip
	env/bin/pip install -U pip
	# устанавливаем основные + dev зависимости из extras_require (см. setup.py)
	env/bin/pip install -Ue '.[dev]'

postgres:
	docker stop disk-postgres || true
	docker run --rm --detach --name=disk-postgres \
		--env POSTGRES_USER=user \
		--env POSTGRES_PASSWORD=hackme \
		--env POSTGRES_DB=disk \
		--publish 5432:5432 postgres

test:
	python3 tests/unit_test.py 

sdist: clean
	# официальный способ дистрибуции python-модулей
	python3 setup.py sdist

docker: sdist
	docker build --target=api -t $(PROJECT_NAME):$(VERSION) .

upload: docker
	docker tag $(PROJECT_NAME):$(VERSION) $(REGISTRY_IMAGE):$(VERSION)
	docker tag $(PROJECT_NAME):$(VERSION) $(REGISTRY_IMAGE):latest
	docker push $(REGISTRY_IMAGE):$(VERSION)
	docker push $(REGISTRY_IMAGE):latest
