import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
import torch
import json
import os
import hashlib
import random
import pretrainedmodels

from datetime import datetime
from PIL import Image
from statistics import mean

from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

from torch import nn, optim
from torchvision.transforms.functional import to_tensor
from torchvision import datasets, transforms, models
from torchvision.utils import save_image
from torch.utils.data import DataLoader, Dataset
from tqdm.auto import tqdm

from pretrainedmodels.models.xception import Xception
from custom_models.MobileNetV2 import MobileNetV2
  
  
# Helpful functions that can be used throughout 
def get_timestamp():
    '''Creates a timestamp, typically useful for generating unique file names for models and images.'''
    
    now = datetime.now()
    timestamp = now.strftime("%d.%m.%Y %H:%M:%S,%f")
    return timestamp


def reload_models(model, model_dir, folder_name, device="cuda", debug=False):
    '''Reloads multiple models based on a directory passed through.'''
    
    models = []

    print('Reading in models...')
    path = os.path.join(model_dir, folder_name)
    for i, (subdir, dirs, files) in enumerate(os.walk(path)):
        if not files:
            continue

        for f in files:
            if debug:
                print(f'Reading {f}')
                
            model = model.to(device)
            model.load_state_dict(state_dict=torch.load(subdir+'/'+f)['model_state_dict'])
            models.append(model)

    return models


def clear_dirs(dir):
    '''Clears out files in a directory.'''
    
    walk = list(os.walk(dir))
    walk.sort()
    for i, (subdir, dirs, files) in enumerate(walk):
        if not files:
            continue
        
        for f in files:
            os.remove(subdir+"/"+f)
            

def create_fold_dirs(target_dir, dir_names):
    '''Creates fold directories.'''
    
    for d in dir_names:
        try:
            os.makedirs(target_dir+'/'+d)
        except FileExistsError:
            continue
    
        
def create_fold_names(model_name, n_splits=5):
    return [f"{model_name}_fold_{idx}" for idx in range(1, n_splits+1)]

            
def remove_outliers(data, constant=1.5):
    '''Removes outliers from a given dataset. Must be numerical.'''
    
    data.sort()
    upper_quartile = np.percentile(data, 75, interpolation="nearest")
    lower_quartile = np.percentile(data, 25, interpolation="nearest")
    iqr = upper_quartile - lower_quartile
    l_outlier = lower_quartile - (constant * iqr)
    u_outlier = upper_quartile + (constant * iqr)
    data_clean = [d for d in data if d >= l_outlier and d <= u_outlier]
  
    return np.array(data_clean)


def time_to_predict(model, loader, constant=1.5, device="cuda:0"):
    '''Calculates the time to predict on a dataset and removes outliers.'''
    
    deltas = []
        
    for images, labels in tqdm(loader, desc="Predicting...".title()):
        images = images.to(device, dtype=torch.float)
        labels = labels.to(device, dtype=torch.long)
        start = datetime.now()
        model(images).to(device, dtype=torch.long) # we don't care about the output
        end = datetime.now()
        delta = (end - start).total_seconds() * 1000
        deltas.append(delta)

    deltas = remove_outliers(deltas)
        
    print(f'\nNumber of Predictions:{len(deltas)}\tClassification Time Mean: {np.mean(deltas):.4f}ms\tClassification Time Max: {np.max(deltas):.4f}ms\tClassification Time Min: {np.min(deltas):.4f}ms')
    return deltas


def random_sampling(dataset, num_of_classes=2, num_of_images=1000):
    ''' This is going to figure out how many additional images to add to the dataset '''

    balanced_data = list()
    for i in range(num_of_classes):
        num_of_additional_imgs = num_of_images - len(dataset[i])
        for j in range(num_of_additional_imgs):
            dataset[i].append(random.choice(dataset[i]))
            
        balanced_data += dataset[i]

    return balanced_data



class CustomXception(Xception):
    def __init__(self, num_of_classes=2, debug=False):
        super().__init__()
        self.fc = nn.Linear(self.fc.in_features, num_of_classes)
        self.last_linear = self.fc
        del self.fc
        if debug:
            print(self)
      
    def forward(self, x):
        return super().forward(x)



class CustomDataset(Dataset):
    def __init__(self, train_utils, mode="train"):
        super().__init__()
        folds, X, y = train_utils.split_data_and_create_folds()
        self.folds = folds
        self.X = X
        self.y = y
        self.train_transform = train_utils.train_transform
        self.test_transform = train_utils.test_transform
        self.mode = mode

    def __getitem__(self, index):
        item = self.X[index]
        label = self.y[index]
        item = transforms.ToPILImage()(item)
            
        if self.mode == "train":
            return (self.train_transform(item), label) if self.train_transform else (item, label)
        else:
            return (self.test_transform(item), label) if self.test_transform else (item, label)

        
    def change_mode(self, new_mode):
        self.mode = new_mode


    def __len__(self):
        return len(self.X)

  
  
class DataVizUtilities:
    '''All of the functions used for displaying graphical data and/or helper functions to display images. Best used with Computer Vision.'''
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    
    def im_convert(self, tensor, mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)):
        '''Converts an image so it can be displayed using matplotlib functions properly.'''
        
        image = tensor.clone().detach().numpy()
        image = image.transpose(1, 2, 0)
        image = image * np.array(std) + np.array(mean) # [0, 1] -> [0, 255]
        image = image.clip(0, 1)
        return image
    

    def display_dataset(self, train_utils):
        '''Displays the dataset. Useful for making sure your data was loaded properly.'''
        
        print(train_utils.mode)
        dataiter = iter(train_utils.loader)
        images, labels = dataiter.next()
        print(images.shape)
        fig = plt.figure(figsize=(25, 4))

        for idx in np.arange(min(train_utils.batch_size, 20)):
            ax = fig.add_subplot(2, 10, idx+1, xticks=[], yticks=[])
            plt.imshow(self.im_convert(images[idx], mean=train_utils.mean, std=train_utils.std))
            ax.set_title(train_utils.classes[labels[idx].numpy()])
                
    
    def display_metric_results(self, train_utils, fold, figsize=(7, 7), device="cuda", img_dir=None):
        '''Displays classification report and confusion matrix.'''
        
        with torch.no_grad():
            y_pred, y_true = train_utils.get_predictions(fold, img_dir=img_dir)
            
        y_true = torch.tensor(y_true).to(device, dtype=torch.long)
        xticks = yticks = train_utils.classes
        
        print("Classification Report\n")
        print(classification_report(y_true.cpu(), y_pred.argmax(dim=1).cpu(), target_names=xticks))
        print("Confusion Matrix")
        cnf_mat = confusion_matrix(y_true.cpu(), y_pred.argmax(dim=1).cpu())

        # plot
        plt.figure(figsize=figsize)
        sns.heatmap(cnf_mat, xticklabels=xticks, yticklabels=yticks, annot=True, cmap="Blues_r")
        plt.ylabel('Ground Truth')
        plt.xlabel('Predictions')
        plt.title("Confusion Matrix " + train_utils.model_name)
        plt.show()  
        
        
    def display_results(self, loss, acc, val_loss, val_acc, title, figsize=(7, 7)):
        '''Displays the accuracy and loss training results.'''
            
        plt.figure(figsize=figsize)
        plt.subplot(2, 1, 1)

        plt.plot(acc, label='Training Accuracy', color='blue')
        plt.plot(val_acc, label='Validation Accuracy', color='lightseagreen')
        plt.legend(loc='lower right')
        plt.ylabel('Accuracy')
        plt.ylim([0, 1.2])
        plt.title('Training and Validation Accuracy '+ title)

        y_upper_bound = max(max(loss), max(val_loss))
        plt.subplot(2, 1, 2)
        plt.plot(loss, label='Training Loss', color='blue')
        plt.plot(val_loss, label='Validation Loss', color='lightseagreen')
        plt.legend(loc='upper right')
        plt.ylabel('Cross Entropy')
        plt.ylim([0, y_upper_bound+y_upper_bound*0.2])
        plt.title('Training and Validation Loss '+ title)
        plt.xlabel('epoch')
        plt.show() 
        
        
    def display_benchmark_results(self, deltas1, deltas2, d1_name, d2_name, model_name, shade=True, legend=True, bw_adjust=5):
        '''Displays benchmark prediction times.'''
        
        plt.figure(figsize=(7, 7))
        x_max = max(max(deltas1), max(deltas2))
        sns.kdeplot(x=deltas1, color="blue", shade=shade, label=d1_name, bw_adjust=bw_adjust)
        sns.kdeplot(x=deltas2, color="purple", shade=shade, label=d2_name, bw_adjust=bw_adjust)
        
        plt.xlabel('Time (ms)')
        plt.xlim([0, x_max+x_max*0.3])
        plt.title(f'Benchmark Results for {model_name}')
        plt.legend(loc="upper right")
        plt.show()

        
    def display_roc_curve(self, train_utils, figsize=(7, 7)):
        '''Displays ROC curve.'''
        
        with torch.no_grad():
            y_pred, y_true = train_utils.get_predictions(0, img_dir="")
            y_pred, y_true = y_pred.argmax(dim=1).cpu().numpy(), torch.tensor(y_true).cpu().numpy()
        
        fpr, tpr, thresholds = roc_curve(y_pred, y_true)
        roc_auc = auc(fpr, tpr)
        
        plt.figure(figsize=figsize)
        plt.plot(fpr, tpr, linewidth=2, label=train_utils.model_name+f" area: {roc_auc:.4f}", color='blue')
        # sns.lineplot(fpr, tpr, label=label+" area", color='blue')
        plt.plot([0, 1], [0, 1], 'k--')
        plt.axis([0, 1, 0, 1])
        plt.xlim([-0.02, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.legend(loc="lower right")
        plt.show()



class Training_Utilities:
    '''Useful functions for training PyTorch models. Geared towards Computer Vision.'''
    def __init__(self, data_dir, parameters_path="parameters.json", model_name="mobilenetv2", mode="train"):
        self.model = nn.Module()
        self.data_dir = data_dir
        self.parameters_path = parameters_path
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # VARIABLE INITIALIZATION
        self.model_name = model_name
        self.classes = []
        self.batch_size = 0
        self.eta = 0
        self.patience = 0
        self.crop_size = 0
        self.degrees = 0
        self.hue = 0
        self.saturation = 0
        self.contrast = 0
        self.brightness = 0
        self.monitor = ""
        self.min_delta = float("inf")
        self.lr_patience = 0
        self.factor = 0
        self.n_splits = 0
        self.input_size = []
        self.mean = []
        self.std = []
        self.train_transform = None
        self.test_transform = None
        self.sign_dataset = None
        self.loader = None
        self.mode = mode
        self.change_model_parameters(self.model_name, mode=self.mode)
        
        
    def change_model_parameters(self, model_name, mode="train"):
        ''' Switch the model parameters based on which model architecture we're using. '''
        with open(self.parameters_path, "r") as f:
            json_file = json.load(f)
            self.classes = json_file["CLASSES"]
            self.n_splits = json_file["N_SPLITS"]
            settings = json_file[model_name]
            
        print(settings)

        # HYPERPARAMETERS
        self.model_name = model_name
        self.batch_size = settings["BATCH_SIZE"]
        self.eta = settings["ETA"]
        self.patience = settings["PATIENCE"]
        self.crop_size = settings["CROP_SIZE"]
        self.degrees = settings["DEGREES"]
        self.hue = settings["HUE"]
        self.saturation = settings["SATURATION"]
        self.contrast = settings["CONTRAST"]
        self.brightness = settings["BRIGHTNESS"]
        self.monitor = settings["MONITOR"]
        self.min_delta = settings["MIN_DELTA"]
        self.lr_patience = settings["LR_PATIENCE"]
        self.factor = settings["FACTOR"]
        self.input_size = settings["INPUT_SIZE"]
        self.mean = settings["MEAN"]
        self.std = settings["STD"]
        self.mode = mode
        
        self.train_transform = transforms.Compose([transforms.Resize(self.input_size),
                                                   transforms.ColorJitter(hue=self.hue, brightness=self.brightness,
                                                                          saturation=self.saturation, contrast=self.contrast),
                                                    transforms.CenterCrop(self.crop_size),
                                                    transforms.RandomRotation(degrees=self.degrees),
                                                    transforms.RandomPerspective(p=1.0), # we always want a bit of distortion
                                                    transforms.ToTensor(),
                                                    transforms.Normalize(mean=self.mean, std=self.std)])
        
        self.test_transform = transforms.Compose([transforms.Resize(self.input_size),
                                                  transforms.CenterCrop(self.crop_size),
                                                  transforms.ToTensor(),
                                                  transforms.Normalize(mean=self.mean, std=self.std)])
                                        
        self.sign_dataset = CustomDataset(self, mode=self.mode)
        self.loader = self.create_loader(self.sign_dataset, batch_size=self.batch_size, shuffle=True)
    
        
    def update_test_transform(self, new_transform):
        self.test_transform = new_transform
        
    
    def change_mode(self, new_mode):
        self.mode = new_mode
        self.loader.dataset.mode = new_mode


    def load_weights(self, model_name, model_weights, mode="test"):
        weights = torch.load(model_weights)["model_state_dict"]
        self.change_model_parameters(model_name, mode=mode)
        
        if model_name == "mobilenetv2":
            self.model = MobileNetV2(n_class=len(self.classes)).to(self.device)
        
        elif model_name == "xception":
            self.model = CustomXception(num_of_classes=len(self.classes)).to(self.device)
            
        self.model.load_state_dict(weights)
        self.model.eval()
        print("Model in eval mode.")
        

    def create_loader(self, dataset, batch_size=16, shuffle=True):
        '''Creates loader given a dataset.'''
        return torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)
    

    def to_categorical(self):
        '''Converts the labels from names to integers'''
        
        labels = np.array(self.classes)
        label_encoder = LabelEncoder()
        integer_encoded = label_encoder.fit_transform(labels)
        
        onehot_encoder = OneHotEncoder(sparse=False)
        integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
        return onehot_encoder.fit_transform(integer_encoded)
        
    
    def split_data_and_create_folds(self):
        '''Creates dataset and creates splits for k-fold cross validation.'''
        
        X = [] # features
        y = [] # labels

        walk = list(os.walk(self.data_dir))
        walk.sort()
        for i, (subdir, dirs, files) in enumerate(walk):
            if not files:
                continue

            print(f'Creating {subdir}...')
            for idx, f in enumerate(files):
                img = Image.open(subdir+'/'+f)
                img = img.resize(size=self.input_size)
                img = img.convert('RGB')
                img = np.asarray(img)
                X.append(img)
                y.append(i-1)

        print(f'{len(X)} total images loaded')
        folds = list(StratifiedKFold(n_splits=self.n_splits, shuffle=True).split(X, y))
        return folds, np.array(X), np.array(y)
    
    
    def _loop_fn(self, dataset, loader, criterion, optimizer, device="cuda", ascii_=False):
        '''The function that actually does the loop for training. Likely isn't used directly, refer to the `train` function.'''
        
        if self.mode == "train":
            self.model.train()
        elif self.mode == "test":
            self.model.eval()

        cost = correct = 0
        for feature, target in tqdm(loader, ascii=ascii_, desc=self.mode.title()):
            feature, target = feature.to(device, dtype=torch.float32), target.to(device, dtype=torch.long)
            output = self.model(feature)
            loss = criterion(output, target)
            self.model.metric = loss
            
            if self.mode == "train":
                loss.backward()
                optimizer.step()
                optimizer.zero_grad()

            cost += loss.item() * feature.shape[0]
            correct += (output.argmax(1) == target).sum().item()

        cost = cost / len(dataset)
        acc = correct / len(dataset)
        return cost, acc
        
    
    @torch.no_grad() # https://deeplizard.com/learn/video/0LhiS6yu2qQ
    def get_predictions(self, fold, device="cuda", img_dir=None):
        '''Gets all of the predictions. Useful for determining model performance.'''
        
        y_pred = torch.tensor([]).to(device, dtype=torch.long)
        y_true = torch.tensor([]).to(device, dtype=torch.long)
        
        for images, labels in self.loader:
            images = images.to(device, dtype=torch.float32)
            labels = labels.to(device, dtype=torch.long)
            target = labels.to(device, dtype=torch.long).cpu().numpy()[0]
            
            pred = self.model(images).to(device, dtype=torch.long)
            y_pred = torch.cat((y_pred, pred), dim=0)
            y_true = torch.cat((y_true, labels), dim=0)
            
            corrects = (labels == pred.argmax(1))
            for idx, is_correct in enumerate(corrects.cpu().numpy()):
                if img_dir and not is_correct:
                    tensor_img = transforms.ToTensor()(DataVizUtilities().im_convert(tensor=images[idx].cpu(), mean=self.mean, std=self.std))
                    hash_ = hashlib.sha256(get_timestamp().encode('utf-8')).hexdigest()[:5]
                    save_image(tensor_img, img_dir+f"/{self.model_name}_fold_{fold}/{hash_}_{labels[idx]}.png")
                                     
        return y_pred, y_true
    
    
    def train(self, model_name, model_path, inc_path, show_graphs=True, dry_run=True):
        self.change_model_parameters(model_name=model_name)
        
        dir_names = create_fold_names(self.model_name, n_splits=self.n_splits)
        create_fold_dirs(inc_path, dir_names)
        losses = []
        accuracies = []
        
        if dry_run:
            for fold, (train_idx, test_idx) in enumerate(self.sign_dataset.folds):
                print('\nFold ', fold+1)
                if model_name == "xception":
                    self.model = CustomXception(num_of_classes=len(self.classes)).to(self.device)
                    
                elif model_name == "mobilenetv2":
                    self.model = MobileNetV2(n_class=len(self.classes)).to(self.device)
                    
                else:
                    raise Exception("Unknown model name.")
                
                train_idx, test_idx = self.sign_dataset.folds[fold]
                train_dataset = torch.utils.data.Subset(self.sign_dataset, train_idx)
                test_dataset = torch.utils.data.Subset(self.sign_dataset, test_idx)
                
                train_dataset.transform = self.train_transform
                test_dataset.transform = self.test_transform
                
                criterion = nn.CrossEntropyLoss()
                optimizer = torch.optim.Adam(self.model.parameters(), lr=self.eta)
                lr_scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=self.factor, patience=self.lr_patience, verbose=True)
                loss, acc = self._train(train_dataset, test_dataset, model_path, criterion, optimizer, fold+1, ascii_=True, scheduler=lr_scheduler, 
                                        dry_run=dry_run, show_graphs=show_graphs, inc_path=inc_path)
                
                losses.append(loss)
                accuracies.append(acc)
                
            avg_loss = mean(losses)
            avg_acc = mean(accuracies)
            print(f'Average Loss: {avg_loss:.5f}  |  Average Accuracy: {avg_acc:.5f}')
            return avg_loss, avg_acc
            
        else:
            if self.model_name == "xception":
                self.model = CustomXception(num_of_classes=len(self.classes)).to(self.device)
            elif self.model_name == "mobilenetv2":
                self.model = MobileNetV2(n_class=len(self.classes)).to(self.device)
            else:
                raise Exception("Unknown model name.")
            
            fold = 0
            train_idx, test_idx = self.sign_dataset.folds[fold]
            train_dataset = torch.utils.data.Subset(self.sign_dataset, train_idx)
            test_dataset = torch.utils.data.Subset(self.sign_dataset, test_idx)
            criterion = nn.CrossEntropyLoss()
            optimizer = torch.optim.Adam(self.model.parameters(), lr=self.eta)
            lr_scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=self.factor, patience=self.lr_patience, verbose=True)
            loss, acc = self._train(train_dataset, test_dataset, model_path, criterion, optimizer, fold+1, ascii_=True, scheduler=lr_scheduler, dry_run=dry_run, show_graphs=show_graphs, inc_path=inc_path)
            losses.append(loss)
            accuracies.append(acc)
            
            avg_loss = mean(losses)
            avg_acc = mean(accuracies)
            print(f'Average Loss: {avg_loss:.5f}  |  Average Accuracy: {avg_acc:.5f}')
            return avg_loss, avg_acc
    
    
    # https://stackoverflow.com/questions/58996242/cross-validation-for-mnist-dataset-with-pytorch-and-sklearn
    def _train(self, train_dataset, test_dataset, filepath, criterion, optimizer, fold, max_epoch=1000, scheduler=None, shuffle=True, device="cuda", 
              ascii_=False, show_graphs=True, dry_run=False, inc_path=""):
        '''Does the actual training. Implements early stopping and some debugging.'''
        
        early_stopping = EarlyStopping(filepath, fold, min_delta=self.min_delta, model_name=self.model_name)
        train_total_loss = []
        train_total_acc = []
        val_total_loss = []
        val_total_acc = []
        test_loader = self.create_loader(test_dataset, batch_size=self.batch_size, shuffle=shuffle)
        train_loader = self.create_loader(train_dataset, batch_size=self.batch_size, shuffle=shuffle)
            
        epoch = 1
        for e in range(max_epoch):
            print(f'\nEpoch {fold}.{epoch}')
            self.change_mode("train")
            train_cost, train_score = self._loop_fn(train_dataset, train_loader, criterion, optimizer, device, ascii_=ascii_)
            with torch.no_grad():
                self.change_mode("test")
                test_cost, test_score = self._loop_fn(test_dataset, test_loader, criterion, optimizer, device, ascii_=ascii_)
                
            if scheduler:
                scheduler.step(test_cost)
                
            train_total_loss.append(train_cost)
            train_total_acc.append(train_score)
            val_total_loss.append(test_cost)
            val_total_acc.append(test_score)
                
            es_counter = early_stopping.checkpoint(self.model, epoch, test_cost, test_score, optimizer, dry_run=dry_run)
            print(f'\nTrain Loss: {train_cost:.3f}   | Train Acc: {train_score:.4f}  | Val Loss: {test_cost:.3f}   | Val Acc: {test_score:.4f}')
            print(f'Early Stopping Patience at: {es_counter}')
                
            if es_counter == self.patience:
                if show_graphs:
                    self.model.eval()
                    DataVizUtilities().display_results(train_total_loss, train_total_acc, val_total_loss, val_total_acc, 
                                                       title=early_stopping.model_name)
                    
                    DataVizUtilities().display_metric_results(train_utils=self, fold=fold, img_dir=inc_path)
                    
                break
            
            epoch += 1
            
        return early_stopping.min_loss, early_stopping.max_acc
    
  
                   
class EarlyStopping():
    '''Class for early stopping, because only plebs rely on set amounts of epochs.'''
    
    def __init__(self, filepath, fold, model_name="", min_delta=0):
        
        self.filepath = filepath
        self.min_loss = float('inf')
        self.max_acc = -float('inf')
        self.min_delta = min_delta
        hash_ = hashlib.sha256(get_timestamp().encode('utf-8')).hexdigest()[:3]
        self.model_name = model_name 
        self.path = str(os.path.join(self.filepath, self.model_name+'.pth'))
        self.count = 0
        self.first_run = True
        self.best_model = None
        
    def checkpoint(self, model, epoch, loss, acc, optimizer, dry_run=False):
        '''Creates the checkpoint and keeps track of when we should stop training. You can choose whether or not you'd like to save the model based on the `dry_run` parameter.'''
        
        print(f'Loss to beat: {(self.min_loss - self.min_delta):.4f}')
        if (self.min_loss - self.min_delta) > loss or self.first_run:
            self.first_run = False
            self.min_loss = loss
            self.max_acc = acc
            self.best_model = model
            self.count = 0
            if not dry_run:
                torch.save({'epoch': epoch,
                            'model_state_dict': model.state_dict(),
                            'optimizer_state_dict': optimizer.state_dict(),
                            'loss': loss,}, self.path)
            
        else:
            self.count += 1
            
        return self.count
   
             