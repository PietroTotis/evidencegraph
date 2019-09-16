# -*- coding: utf-8 -*-

'''
@author: Andreas Peldszus
'''

folds = [
    ['micro_k009', 'micro_b050', 'micro_b055', 'micro_b041', 'micro_b036', 'micro_b007', 'micro_k021', 'micro_d08', 'micro_b033', 'micro_b060', 'micro_b034', 'micro_k003', 'micro_d15', 'micro_d20', 'micro_k012', 'micro_d13', 'micro_b010', 'micro_k029', 'micro_d14', 'micro_b024', 'micro_b009', 'micro_k011'],
    ['micro_k001', 'micro_d11', 'micro_b058', 'micro_k014', 'micro_b029', 'micro_d03', 'micro_d07', 'micro_b002', 'micro_k023', 'micro_b049', 'micro_d01', 'micro_k006', 'micro_b031', 'micro_d12', 'micro_k024', 'micro_k017', 'micro_b054', 'micro_b012', 'micro_b062', 'micro_b052', 'micro_k008', 'micro_d21', 'micro_b016'],
    ['micro_k031', 'micro_b018', 'micro_k010', 'micro_k025', 'micro_b040', 'micro_d06', 'micro_b061', 'micro_b039', 'micro_d02', 'micro_b045', 'micro_b008', 'micro_b032', 'micro_b059', 'micro_k013', 'micro_b047', 'micro_k002', 'micro_b053', 'micro_b044', 'micro_b023', 'micro_d19', 'micro_b030', 'micro_b025', 'micro_b003'],
    ['micro_b051', 'micro_k007', 'micro_k019', 'micro_b019', 'micro_b042', 'micro_b027', 'micro_b046', 'micro_b057', 'micro_d16', 'micro_b006', 'micro_k018', 'micro_b015', 'micro_d17', 'micro_d18', 'micro_b004', 'micro_k020', 'micro_b001', 'micro_b028', 'micro_b011', 'micro_b017', 'micro_k022', 'micro_b013'],
    ['micro_b056', 'micro_d23', 'micro_b038', 'micro_d04', 'micro_d05', 'micro_b005', 'micro_k027', 'micro_b026', 'micro_k004', 'micro_b020', 'micro_b014', 'micro_d22', 'micro_b021', 'micro_b048', 'micro_b022', 'micro_k015', 'micro_b037', 'micro_b035', 'micro_d10', 'micro_d09', 'micro_k016', 'micro_b064'],
    ['micro_b056', 'micro_b018', 'micro_b058', 'micro_k025', 'micro_b042', 'micro_b027', 'micro_b046', 'micro_b057', 'micro_b002', 'micro_b049', 'micro_d01', 'micro_b060', 'micro_b031', 'micro_d12', 'micro_b054', 'micro_b004', 'micro_k012', 'micro_d10', 'micro_b035', 'micro_b009', 'micro_b064', 'micro_k016', 'micro_d21'],
    ['micro_k031', 'micro_d11', 'micro_b038', 'micro_k014', 'micro_b040', 'micro_b005', 'micro_b053', 'micro_b020', 'micro_b033', 'micro_k004', 'micro_b034', 'micro_k003', 'micro_d15', 'micro_k029', 'micro_k024', 'micro_b001', 'micro_b052', 'micro_b010', 'micro_d14', 'micro_b023', 'micro_b003', 'micro_b025', 'micro_b016'],
    ['micro_k001', 'micro_d23', 'micro_k010', 'micro_b041', 'micro_b036', 'micro_b007', 'micro_k021', 'micro_k027', 'micro_k023', 'micro_b014', 'micro_b047', 'micro_k006', 'micro_b021', 'micro_b048', 'micro_d13', 'micro_k020', 'micro_b037', 'micro_k015', 'micro_b028', 'micro_b030', 'micro_d09', 'micro_b013'],
    ['micro_b051', 'micro_k007', 'micro_b055', 'micro_b019', 'micro_b029', 'micro_d03', 'micro_b061', 'micro_b026', 'micro_d02', 'micro_b045', 'micro_b008', 'micro_b032', 'micro_b059', 'micro_d20', 'micro_k013', 'micro_b022', 'micro_k017', 'micro_b017', 'micro_b062', 'micro_k008', 'micro_k022', 'micro_b012'],
    ['micro_k009', 'micro_b050', 'micro_k019', 'micro_d04', 'micro_d05', 'micro_d06', 'micro_d07', 'micro_b039', 'micro_d16', 'micro_b006', 'micro_k018', 'micro_b015', 'micro_d17', 'micro_d18', 'micro_d08', 'micro_k002', 'micro_d22', 'micro_b044', 'micro_d19', 'micro_b024', 'micro_b011', 'micro_k011'],
    ['micro_k001', 'micro_d11', 'micro_b038', 'micro_b041', 'micro_b042', 'micro_b007', 'micro_k021', 'micro_k027', 'micro_b002', 'micro_b045', 'micro_d01', 'micro_b060', 'micro_d15', 'micro_k029', 'micro_d08', 'micro_k020', 'micro_d10', 'micro_b044', 'micro_b028', 'micro_d19', 'micro_b064', 'micro_b003'],
    ['micro_k031', 'micro_b050', 'micro_k019', 'micro_b019', 'micro_b036', 'micro_b027', 'micro_b046', 'micro_b057', 'micro_k023', 'micro_b049', 'micro_b008', 'micro_k006', 'micro_b021', 'micro_d20', 'micro_k012', 'micro_b054', 'micro_d22', 'micro_b052', 'micro_d14', 'micro_b024', 'micro_k008', 'micro_b062', 'micro_b012'],
    ['micro_k009', 'micro_k007', 'micro_b055', 'micro_k025', 'micro_b040', 'micro_b005', 'micro_b061', 'micro_b026', 'micro_d02', 'micro_b014', 'micro_b047', 'micro_b032', 'micro_b059', 'micro_k013', 'micro_k024', 'micro_d12', 'micro_d13', 'micro_b010', 'micro_b009', 'micro_b017', 'micro_k022', 'micro_b016', 'micro_d21'],
    ['micro_b051', 'micro_d23', 'micro_b058', 'micro_k014', 'micro_b029', 'micro_d03', 'micro_b053', 'micro_b020', 'micro_b033', 'micro_k004', 'micro_b034', 'micro_b015', 'micro_b031', 'micro_b048', 'micro_b022', 'micro_k015', 'micro_k017', 'micro_b035', 'micro_b013', 'micro_d09', 'micro_b030', 'micro_k011'],
    ['micro_b056', 'micro_b018', 'micro_k010', 'micro_d04', 'micro_d05', 'micro_d06', 'micro_d07', 'micro_b039', 'micro_d16', 'micro_b006', 'micro_k018', 'micro_k003', 'micro_d17', 'micro_d18', 'micro_b004', 'micro_k002', 'micro_b001', 'micro_b037', 'micro_b023', 'micro_b011', 'micro_b025', 'micro_k016'],
    ['micro_k031', 'micro_k007', 'micro_b055', 'micro_b019', 'micro_b029', 'micro_d03', 'micro_d07', 'micro_b002', 'micro_d16', 'micro_b006', 'micro_b014', 'micro_b015', 'micro_d15', 'micro_d17', 'micro_k017', 'micro_b001', 'micro_k022', 'micro_b017', 'micro_d19', 'micro_b023', 'micro_b011', 'micro_b013', 'micro_d21'],
    ['micro_b056', 'micro_b050', 'micro_k019', 'micro_d04', 'micro_d05', 'micro_d06', 'micro_k027', 'micro_b026', 'micro_d02', 'micro_b049', 'micro_b047', 'micro_b032', 'micro_b059', 'micro_k012', 'micro_k018', 'micro_d13', 'micro_b009', 'micro_k002', 'micro_b044', 'micro_k008', 'micro_b030', 'micro_b025'],
    ['micro_b051', 'micro_d11', 'micro_k010', 'micro_b041', 'micro_b042', 'micro_b007', 'micro_b046', 'micro_d08', 'micro_b033', 'micro_b060', 'micro_b008', 'micro_b031', 'micro_k013', 'micro_d20', 'micro_b037', 'micro_k020', 'micro_d22', 'micro_d18', 'micro_k015', 'micro_b035', 'micro_k016', 'micro_b064'],
    ['micro_k009', 'micro_d23', 'micro_b038', 'micro_k014', 'micro_b040', 'micro_b005', 'micro_b061', 'micro_b039', 'micro_k004', 'micro_b020', 'micro_b034', 'micro_k003', 'micro_b021', 'micro_b048', 'micro_b054', 'micro_b053', 'micro_b052', 'micro_b062', 'micro_d14', 'micro_b028', 'micro_b003', 'micro_k011'],
    ['micro_k001', 'micro_b018', 'micro_b058', 'micro_k025', 'micro_b036', 'micro_b027', 'micro_k021', 'micro_b057', 'micro_k023', 'micro_b045', 'micro_d01', 'micro_k006', 'micro_b022', 'micro_k029', 'micro_k024', 'micro_d12', 'micro_b004', 'micro_b010', 'micro_d10', 'micro_b024', 'micro_b012', 'micro_d09', 'micro_b016'],
    ['micro_b051', 'micro_d11', 'micro_b058', 'micro_k025', 'micro_b036', 'micro_b007', 'micro_k021', 'micro_b057', 'micro_k023', 'micro_b020', 'micro_k003', 'micro_k018', 'micro_d17', 'micro_b048', 'micro_b054', 'micro_b053', 'micro_d10', 'micro_b035', 'micro_k015', 'micro_b024', 'micro_b001', 'micro_d09'],
    ['micro_b056', 'micro_d23', 'micro_k010', 'micro_k014', 'micro_d05', 'micro_d06', 'micro_k027', 'micro_b039', 'micro_d02', 'micro_b045', 'micro_d01', 'micro_b032', 'micro_b059', 'micro_d20', 'micro_k012', 'micro_k002', 'micro_b013', 'micro_b052', 'micro_d18', 'micro_b023', 'micro_b012', 'micro_d21', 'micro_k011'],
    ['micro_k031', 'micro_k007', 'micro_b055', 'micro_b041', 'micro_b042', 'micro_b027', 'micro_b046', 'micro_d08', 'micro_b033', 'micro_b060', 'micro_b008', 'micro_b031', 'micro_k006', 'micro_k013', 'micro_b047', 'micro_k020', 'micro_b009', 'micro_b017', 'micro_b028', 'micro_b016', 'micro_k008', 'micro_b025', 'micro_b030'],
    ['micro_k009', 'micro_b050', 'micro_k019', 'micro_b019', 'micro_b029', 'micro_d03', 'micro_d07', 'micro_b002', 'micro_d16', 'micro_b006', 'micro_b034', 'micro_b015', 'micro_b021', 'micro_k029', 'micro_b022', 'micro_b044', 'micro_k017', 'micro_b004', 'micro_b062', 'micro_d14', 'micro_b064', 'micro_b003'],
    ['micro_k001', 'micro_b018', 'micro_b038', 'micro_d04', 'micro_b040', 'micro_b005', 'micro_b061', 'micro_b026', 'micro_k004', 'micro_b049', 'micro_b014', 'micro_d22', 'micro_d15', 'micro_d12', 'micro_k024', 'micro_d13', 'micro_b037', 'micro_b010', 'micro_b011', 'micro_d19', 'micro_k022', 'micro_k016'],
    ['micro_k031', 'micro_d23', 'micro_k010', 'micro_b019', 'micro_b036', 'micro_b027', 'micro_k021', 'micro_k027', 'micro_d16', 'micro_b006', 'micro_b032', 'micro_b015', 'micro_d17', 'micro_b059', 'micro_k024', 'micro_b001', 'micro_b004', 'micro_d18', 'micro_b028', 'micro_d19', 'micro_b030', 'micro_k011', 'micro_b003'],
    ['micro_k009', 'micro_b018', 'micro_b038', 'micro_k014', 'micro_d05', 'micro_d06', 'micro_d07', 'micro_b026', 'micro_k023', 'micro_b014', 'micro_d01', 'micro_k006', 'micro_b031', 'micro_d12', 'micro_b054', 'micro_d08', 'micro_b037', 'micro_d10', 'micro_b035', 'micro_k015', 'micro_b064', 'micro_b016', 'micro_d21'],
    ['micro_b051', 'micro_d11', 'micro_b058', 'micro_d04', 'micro_b029', 'micro_d03', 'micro_b053', 'micro_b020', 'micro_b033', 'micro_k004', 'micro_k018', 'micro_k003', 'micro_b022', 'micro_b011', 'micro_d13', 'micro_k020', 'micro_k029', 'micro_b044', 'micro_b023', 'micro_b009', 'micro_k016', 'micro_b025'],
    ['micro_b056', 'micro_b050', 'micro_b055', 'micro_k025', 'micro_b040', 'micro_b005', 'micro_b061', 'micro_b039', 'micro_d02', 'micro_b045', 'micro_b034', 'micro_d22', 'micro_d15', 'micro_d20', 'micro_k013', 'micro_k012', 'micro_b010', 'micro_b013', 'micro_b017', 'micro_d09', 'micro_k022', 'micro_b012'],
    ['micro_k001', 'micro_k007', 'micro_k019', 'micro_b041', 'micro_b042', 'micro_b007', 'micro_b046', 'micro_b057', 'micro_b002', 'micro_b049', 'micro_b008', 'micro_b060', 'micro_b021', 'micro_b048', 'micro_b047', 'micro_k002', 'micro_k017', 'micro_b052', 'micro_d14', 'micro_b024', 'micro_k008', 'micro_b062'],
    ['micro_k009', 'micro_k007', 'micro_b055', 'micro_d04', 'micro_b040', 'micro_d06', 'micro_b061', 'micro_b039', 'micro_d02', 'micro_b014', 'micro_d01', 'micro_b032', 'micro_b059', 'micro_d20', 'micro_k013', 'micro_b022', 'micro_k017', 'micro_b017', 'micro_b062', 'micro_d14', 'micro_k022', 'micro_b003'],
    ['micro_k001', 'micro_b050', 'micro_k019', 'micro_k025', 'micro_d05', 'micro_b005', 'micro_d07', 'micro_b026', 'micro_k023', 'micro_b049', 'micro_b047', 'micro_b060', 'micro_b021', 'micro_b048', 'micro_k024', 'micro_d22', 'micro_b052', 'micro_d09', 'micro_b035', 'micro_b011', 'micro_b024', 'micro_b012'],
    ['micro_k031', 'micro_d11', 'micro_b058', 'micro_k014', 'micro_b029', 'micro_d03', 'micro_b053', 'micro_b020', 'micro_b033', 'micro_k004', 'micro_b034', 'micro_b015', 'micro_d15', 'micro_k029', 'micro_d13', 'micro_k002', 'micro_b009', 'micro_b044', 'micro_b010', 'micro_k008', 'micro_d19', 'micro_b025', 'micro_b016'],
    ['micro_b056', 'micro_d23', 'micro_b038', 'micro_b019', 'micro_b036', 'micro_b007', 'micro_k021', 'micro_b057', 'micro_b002', 'micro_b045', 'micro_b008', 'micro_k006', 'micro_b031', 'micro_d12', 'micro_b054', 'micro_b004', 'micro_k012', 'micro_d10', 'micro_b023', 'micro_b030', 'micro_b064', 'micro_k016', 'micro_k011'],
    ['micro_b051', 'micro_b018', 'micro_k010', 'micro_b041', 'micro_b042', 'micro_b027', 'micro_b046', 'micro_k027', 'micro_d16', 'micro_b006', 'micro_k018', 'micro_k003', 'micro_d17', 'micro_d18', 'micro_d08', 'micro_k020', 'micro_b001', 'micro_b037', 'micro_b028', 'micro_k015', 'micro_d21', 'micro_b013'],
    ['micro_b051', 'micro_b018', 'micro_k010', 'micro_b041', 'micro_b042', 'micro_b027', 'micro_k021', 'micro_b057', 'micro_k023', 'micro_b045', 'micro_d01', 'micro_k006', 'micro_b031', 'micro_d20', 'micro_k012', 'micro_b022', 'micro_k008', 'micro_b052', 'micro_b062', 'micro_d14', 'micro_k022', 'micro_b003', 'micro_b016'],
    ['micro_b056', 'micro_b050', 'micro_k019', 'micro_k025', 'micro_b040', 'micro_b005', 'micro_b053', 'micro_b020', 'micro_b033', 'micro_k004', 'micro_b034', 'micro_b015', 'micro_d15', 'micro_k029', 'micro_d13', 'micro_k002', 'micro_b009', 'micro_b044', 'micro_b028', 'micro_b030', 'micro_d19', 'micro_b025'],
    ['micro_k031', 'micro_d11', 'micro_b038', 'micro_k014', 'micro_d05', 'micro_d06', 'micro_d07', 'micro_b026', 'micro_b002', 'micro_b049', 'micro_b047', 'micro_b060', 'micro_b021', 'micro_b048', 'micro_b004', 'micro_k020', 'micro_d22', 'micro_d09', 'micro_b037', 'micro_b023', 'micro_b012', 'micro_b064'],
    ['micro_k009', 'micro_k007', 'micro_b055', 'micro_b019', 'micro_b036', 'micro_b007', 'micro_b046', 'micro_k027', 'micro_d16', 'micro_b006', 'micro_k018', 'micro_k003', 'micro_d17', 'micro_d18', 'micro_d08', 'micro_b010', 'micro_b001', 'micro_k017', 'micro_b035', 'micro_k015', 'micro_d21', 'micro_b013', 'micro_k011'],
    ['micro_k001', 'micro_d23', 'micro_b058', 'micro_d04', 'micro_b029', 'micro_d03', 'micro_b061', 'micro_b039', 'micro_d02', 'micro_b014', 'micro_b008', 'micro_b032', 'micro_b059', 'micro_k013', 'micro_k024', 'micro_d12', 'micro_b054', 'micro_d10', 'micro_b017', 'micro_b024', 'micro_b011', 'micro_k016'],
    ['micro_k001', 'micro_b018', 'micro_k010', 'micro_b019', 'micro_b042', 'micro_b007', 'micro_b046', 'micro_d08', 'micro_b033', 'micro_b006', 'micro_b008', 'micro_b032', 'micro_k006', 'micro_k017', 'micro_b047', 'micro_k020', 'micro_k029', 'micro_b044', 'micro_b028', 'micro_b011', 'micro_k022', 'micro_b003'],
    ['micro_b056', 'micro_k007', 'micro_b055', 'micro_b041', 'micro_b036', 'micro_b027', 'micro_k021', 'micro_b057', 'micro_k023', 'micro_b020', 'micro_k003', 'micro_k018', 'micro_d17', 'micro_k013', 'micro_b022', 'micro_b001', 'micro_k002', 'micro_k015', 'micro_d14', 'micro_b023', 'micro_b013', 'micro_k016'],
    ['micro_k031', 'micro_b050', 'micro_k019', 'micro_k014', 'micro_d05', 'micro_d06', 'micro_k027', 'micro_b039', 'micro_d02', 'micro_b045', 'micro_d01', 'micro_b031', 'micro_b059', 'micro_k012', 'micro_k024', 'micro_d12', 'micro_d18', 'micro_b052', 'micro_b035', 'micro_d10', 'micro_b017', 'micro_d21'],
    ['micro_b051', 'micro_d23', 'micro_b038', 'micro_d04', 'micro_b040', 'micro_b005', 'micro_d07', 'micro_b002', 'micro_d16', 'micro_b060', 'micro_b014', 'micro_d22', 'micro_b021', 'micro_b048', 'micro_b054', 'micro_b053', 'micro_b004', 'micro_b062', 'micro_k008', 'micro_d09', 'micro_b030', 'micro_b064', 'micro_k011'],
    ['micro_k009', 'micro_d11', 'micro_b058', 'micro_k025', 'micro_b029', 'micro_d03', 'micro_b061', 'micro_b026', 'micro_k004', 'micro_b049', 'micro_b034', 'micro_b015', 'micro_d15', 'micro_d20', 'micro_b037', 'micro_d13', 'micro_b010', 'micro_b009', 'micro_d19', 'micro_b024', 'micro_b012', 'micro_b025', 'micro_b016'],
    ['micro_k001', 'micro_d23', 'micro_b058', 'micro_d04', 'micro_b042', 'micro_b027', 'micro_b046', 'micro_k027', 'micro_d16', 'micro_b006', 'micro_b034', 'micro_k003', 'micro_d15', 'micro_k029', 'micro_d13', 'micro_k020', 'micro_b009', 'micro_b044', 'micro_b037', 'micro_b024', 'micro_d19', 'micro_b025'],
    ['micro_b051', 'micro_k007', 'micro_b055', 'micro_b019', 'micro_b029', 'micro_d03', 'micro_b061', 'micro_b026', 'micro_d02', 'micro_b045', 'micro_b008', 'micro_b032', 'micro_b059', 'micro_k013', 'micro_k024', 'micro_d12', 'micro_b054', 'micro_d10', 'micro_b017', 'micro_b023', 'micro_b012', 'micro_k011'],
    ['micro_b056', 'micro_b050', 'micro_k019', 'micro_k014', 'micro_d05', 'micro_d06', 'micro_d07', 'micro_b039', 'micro_k023', 'micro_b014', 'micro_d01', 'micro_k006', 'micro_b021', 'micro_d20', 'micro_k012', 'micro_b022', 'micro_k008', 'micro_b052', 'micro_b062', 'micro_d14', 'micro_k022', 'micro_b003', 'micro_b016'],
    ['micro_k009', 'micro_b018', 'micro_k010', 'micro_b041', 'micro_b036', 'micro_b007', 'micro_k021', 'micro_b057', 'micro_b002', 'micro_b049', 'micro_b047', 'micro_b060', 'micro_b031', 'micro_b048', 'micro_d08', 'micro_b010', 'micro_d22', 'micro_d09', 'micro_b030', 'micro_b028', 'micro_b011', 'micro_b064', 'micro_k016'],
    ['micro_k031', 'micro_d11', 'micro_b038', 'micro_k025', 'micro_b040', 'micro_b005', 'micro_b053', 'micro_b020', 'micro_b033', 'micro_k004', 'micro_k018', 'micro_b015', 'micro_d17', 'micro_d18', 'micro_b004', 'micro_k002', 'micro_b001', 'micro_k017', 'micro_b035', 'micro_k015', 'micro_d21', 'micro_b013']
]

tids = sorted(list(set([tid for fold in folds for tid in fold])))


def get_static_folds():
    for i, test_tids in enumerate(folds):
        train_tids = [tid for tid in tids if tid not in test_tids]
        yield train_tids, test_tids, i
