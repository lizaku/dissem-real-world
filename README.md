* BNC and VG frequency lists can be found in the folder `corpora`.
* Created models are provided in the folder `models`. For VG it is the model with relations.
* Entropix model is created using the command `entropix generate -c corpora/bnc_rawtext.txt -o models -m 10 -w 2`. The minimum frequency is 10, window size is 2.
* PPMI-weighted version of the entropix model is created using the command `entropix weigh -m models/bnc_rawtext.mincount-10.win-2.npz -w ppmi`
* VG model is created by the scripts in the folder `parse_VG`. `parse_data.py` works with the original zipped dataset files and extracts from them relations and attributes. `files2matrices.py` constructs sparse matrix out of created files, `dissect_train.py` creates the dissect space using the sparse matrix.
* words with their clusters can be found in the file `vg_clusters_labels.txt`.
* using the script `get_neighbors_entropix.py` I extract the neighbors from the BNC entropix models and save them as a separate file.
* using the script `compute_neighbors_overlap.py` I load the extracted BNC neighbors, extract the neighbors from the VG model, compute their overlap and save the lists.
