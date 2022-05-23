FROM pfee_base

WORKDIR /root

COPY demo.ipynb .

# CMD ["/bin/bash"]
CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]
